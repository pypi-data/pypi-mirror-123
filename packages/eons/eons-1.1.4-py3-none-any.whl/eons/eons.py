import logging
from abc import ABC
from abc import abstractmethod
import os
import sys
import pkgutil
import operator
import argparse

######## START CONTENT ########
def INVALID_NAME():
    return "INVALID_NAME"


#Self registration for use with json loading.
#Any class that derives from SelfRegistering can be instantiated with:
#   SelfRegistering("ClassName")
#Based on: https://stackoverflow.com/questions/55973284/how-to-create-self-registering-factory-in-python/55973426
class SelfRegistering(object):

    class ClassNotFound(Exception): pass

    def __init__(self, *args, **kwargs):
        #ignore args.
        super().__init__()

    @classmethod
    def GetSubclasses(cls):
        for subclass in cls.__subclasses__():
            # logging.info(f"Subclass dict: {subclass.__dict__}")
            yield subclass
            for subclass in subclass.GetSubclasses():
                yield subclass

    #TODO: How do we pass args to the subsequently called __init__()?
    def __new__(cls, classname, *args, **kwargs):
        for subclass in cls.GetSubclasses():
            if subclass.__name__ == classname:
                logging.debug(f"Creating new {subclass.__name__}")

                # Using "object" base class method avoids recursion here.
                child = object.__new__(subclass)

                #__dict__ is always blank during __new__ and only populated by __init__.
                #This is only useful as a negative control.
                # logging.debug(f"Created object of {child.__dict__}")

                return child
        
        # no subclass with matching classname found (and no default defined)
        raise SelfRegistering.ClassNotFound(f'No known SelfRegistering class: {classname}')

    @staticmethod
    def RegisterAllClassesInDirectory(directory):
        logging.debug(f"Loading SelfRegistering classes in {directory}")
        # logging.debug(f"Available files: {os.listdir(directory)}")
        for importer, file, _ in pkgutil.iter_modules([directory]):
            logging.debug(f"Found {file} with {importer}")
            if file not in sys.modules and file != 'main':
                module = importer.find_module(file).load_module(file)


#A Datum is a base class for any object-oriented data structure.
#This class is intended to be derived from and added to.
#The members of this class are helpful labels along with the ability to invalidate a datum.
class Datum(SelfRegistering):

    #Don't worry about this.
    #If you really want to know, look at SelfRegistering.
    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def __init__(self, name=INVALID_NAME(), number=0):
        # logging.debug("init Datum")

        #Names are generally useful.
        self.name = name

        #Storing validity as a member makes it easy to generate bad return values (i.e. instead of checking for None) as well as manipulate data (e.g. each analysis step invalidates some data and all invalid data are discarded at the end of analysis).
        self.valid = True 

    #Override this if you have your own validity checks.
    def IsValid(self):
        return self.valid == True

    #Sets valid to true
    #Override this if you have members you need to handle with care.
    def MakeValid(self):
        self.valid = True

    #Sets valid to false.
    def Invalidate(self):
        self.valid = False

class MissingArgumentError(Exception):
    pass


#UserFunctor is a base class for any function-oriented data structure or operation.
#This class derives from Datum, primarily, to give it a name but also to allow it to be stored and manipulated, should you so desire.
class UserFunctor(ABC, Datum):

    def __init__(self, name=INVALID_NAME()):
        super().__init__(name)
        self.requiredKWArgs = []

    #Override this and do whatever!
    #This is purposefully vague.
    @abstractmethod
    def UserFunction(self, **kwargs):
        raise NotImplementedError 

    #Override this with any additional argument validation you need.
    #This is called before PreCall(), below.
    def ValidateArgs(self, **kwargs):
        logging.debug(f'kwargs: {kwargs}')
        logging.debug(f'required kwargs: {self.requiredKWArgs}')
        for rkw in self.requiredKWArgs:
            if (rkw not in kwargs):
                logging.error(f'argument {rkw} not found in {kwargs}')
                raise MissingArgumentError(f'argument {rkw} not found in {kwargs}') #TODO: not formatting string??

    #Override this with any logic you'd like to run at the top of __call__
    def PreCall(self, **kwargs):
        pass

    #Override this with any logic you'd like to run at the bottom of __call__
    def PostCall(self, **kwargs):
        pass

    #Make functor.
    #Don't worry about this; logic is abstracted to UserFunction
    def __call__(self, **kwargs) :
        logging.debug(f"{self.name}({kwargs})")
        self.ValidateArgs(**kwargs)
        self.PreCall(**kwargs)
        ret = self.UserFunction(**kwargs)
        self.PostCall(**kwargs)
        return ret


#A DataContainer allows Data to be stored and worked with.
#This class is intended to be derived from and added to.
#Each DataContainer is comprised of multiple Data (see Datum.py for more).
#NOTE: DataContainers are, themselves Data. Thus, you can nest your child classes however you would like.
class DataContainer(Datum):
    def __init__(self, name=INVALID_NAME()):
        super().__init__(name)
        self.data = []

    #RETURNS: an empty, invalid Datum.
    def InvalidDatum(self):
        ret = Datum()
        ret.Invalidate()
        return ret

    #Sort things! Requires by be a valid attribute of all Data.
    def SortData(self, by):
        self.data.sort(key=operator.attrgetter(by))

    #Adds a Datum to *this
    def AddDatum(self, datum):
        self.data.append(datum)

    #RETURNS: a Datum with datumAttribute equal to match, an invalid Datum if none found.
    def GetDatumBy(self, datumAttribute, match):
        for d in self.data:
            try: #within for loop 'cause maybe there's an issue with only 1 Datum and the rest are fine.
                if (str(getattr(d, datumAttribute)) == str(match)):
                    return d
            except Exception as e:
                logging.error(f"{self.name} - {e.message}")
                continue
        return self.InvalidDatum()

    #RETURNS: a Datum of the given name, an invalid Datum if none found.
    def GetDatum(self, name):
        return self.GetDatumBy('name', name)

    #Removes all Data in toRem from *this.
    #RETURNS: the Data removed
    def RemoveData(self, toRem):
        # logging.debug(f"Removing {toRem}")
        self.data = [d for d in self.data if d not in toRem]
        return toRem

    #Removes all Data which match toRem along the given attribute
    def RemoveDataBy(self, datumAttribute, toRem):
        toRem = [d for d in self.data if str(getattr(d, datumAttribute)) in list(map(str, toRem))]
        return self.RemoveData(toRem)

    #Removes all Data in *this except toKeep.
    #RETURNS: the Data removed
    def KeepOnlyData(self, toKeep):
        toRem = [d for d in self.data if d not in toKeep]
        return self.RemoveData(toRem)

    #Removes all Data except those that match toKeep along the given attribute
    #RETURNS: the Data removed
    def KeepOnlyDataBy(self, datumAttribute, toKeep):
        # logging.debug(f"Keeping only data with a {datumAttribute} of {toKeep}")
        # toRem = []
        # for d in self.data:
        #     shouldRem = False
        #     for k in toKeep:
        #         if (str(getattr(d, datumAttribute)) == str(k)):
        #             logging.debug(f"found {k} in {d.__dict__}")
        #             shouldRem = True
        #             break
        #     if (shouldRem):
        #         toRem.append(d)
        #     else:
        #         logging.debug(f"{k} not found in {d.__dict__}")
        toRem = [d for d in self.data if str(getattr(d, datumAttribute)) not in list(map(str, toKeep))]
        return self.RemoveData(toRem)

    #Removes all Data with the name "INVALID NAME"
    #RETURNS: the removed Data
    def RemoveAllUnlabeledData(self):
        toRem = []
        for d in self.data:
            if (d.name =="INVALID NAME"):
                toRem.append(d)
        return self.RemoveData(toRem)

    #Removes all invalid Data
    #RETURNS: the removed Data
    def RemoveAllInvalidData(self):
        toRem = []
        for d in self.data:
            if (not d.IsValid()):
                toRem.append(d)
        return self.RemoveData(toRem)

    #Removes all Data that have an attribute value relative to target.
    #The given relation can be things like operator.le (i.e. <=)
    #   See https://docs.python.org/3/library/operator.html for more info.
    #If ignoreNames is specified, any Data of those names will be ignored.
    #RETURNS: the Data removed
    def RemoveDataRelativeToTarget(self, datumAttribute, relation, target, ignoreNames = []):
        try:
            toRem = []
            for d in self.data:
                if (ignoreNames and d.name in ignoreNames):
                    continue
                if (relation(getattr(d, datumAttribute), target)):
                    toRem.append(d)
            return self.RemoveData(toRem)
        except Exception as e:
            logging.error(f"{self.name} - {e.message}")
            return []

    #Removes any Data that have the same datumAttribute as a previous Datum, keeping only the first.
    #RETURNS: The Data removed
    def RemoveDuplicateDataOf(self, datumAttribute):
        toRem = [] #list of Data
        alreadyProcessed = [] #list of strings, not whatever datumAttribute is.
        for d1 in self.data:
            skip = False
            for dp in alreadyProcessed:
                if (str(getattr(d1, datumAttribute)) == dp):
                    skip = True
                    break
            if (skip):
                continue
            for d2 in self.data:
                if (d1 is not d2 and str(getattr(d1, datumAttribute)) == str(getattr(d2, datumAttribute))):
                    logging.info(f"Removing duplicate Datum {d2} with unique id {getattr(d2, datumAttribute)}")
                    toRem.append(d2)
                    alreadyProcessed.append(str(getattr(d1, datumAttribute)))
        return self.RemoveData(toRem)

    #Adds all Data from otherDataContainer to *this.
    #If there are duplicate Data identified by the attribute preventDuplicatesOf, they are removed.
    #RETURNS: the Data removed, if any.
    def ImportDataFrom(self, otherDataContainer, preventDuplicatesOf=None):
        self.data.extend(otherDataContainer.data);
        if (preventDuplicatesOf is not None):
            return self.RemoveDuplicateDataOf(preventDuplicatesOf)
        return []



#Executor: a base class for user interfaces.
#An Executor is a functor and can be executed as such.
#For example
#   class MyExecutor(Executor):
#       def __init__(self):
#           super().__init__()
#   . . .
#   myprogram = MyExecutor()
#   myprogram()
#NOTE: Diamond inheritance of Datum.
class Executor(DataContainer, UserFunctor):

    def __init__(self, name=INVALID_NAME(), descriptionStr="eons python framework. Extend as thou wilt."):
        self.SetupLogging()
        
        super().__init__(name)
        
        self.argparser = argparse.ArgumentParser(description = descriptionStr)
        self.args = None
        self.extraArgs = None
        self.AddArgs()

        self.registerDirectories = []
        
    #Add a place to search for SelfRegistering classes.
    #These should all be relative to the invoking working directory (i.e. whatever './' is at time of calling Executor())
    def RegisterDirectory(self, directory):
        self.registerDirectories.append(directory)
        
    #Global logging config.
    #Override this method to disable or change.
    def SetupLogging(self):
        logging.basicConfig(level = logging.INFO, format = '%(asctime)s [%(levelname)-8s] - %(message)s (%(filename)s:%(lineno)s)', datefmt = '%H:%M:%S')

    #Adds command line arguments.
    #Override this method to change. Optionally, call super().AddArgs() within your method to simply add to this list.
    def AddArgs(self):
        self.argparser.add_argument('--verbose', '-v', action='count', default=0)

    #Create any sub-data necessary for child-operations
    #Does not RETURN anything.
    def InitData(self):
        pass
        
    #Register all classes in each directory in self.registerDirectories
    def RegisterAllClasses(self):
        for d in self.registerDirectories:
            self.RegisterAllClassesInDirectory(os.path.join(os.getcwd(), d))

    #Something went wrong, let's quit.
    #TODO: should this simply raise an exception?
    def ExitDueToErr(self, errorStr):
        # logging.info("#################################################################\n")
        logging.error(errorStr)
        # logging.info("\n#################################################################")
        self.argparser.print_help()
        sys.exit()

    #Do the argparse thing.
    def ParseArgs(self):
        self.args, self.extraArgs = self.argparser.parse_known_args()

        extraArgsKeys = []
        for index in range(0, len(extraArgs), 2):
            extraArgsKeys.append(extraArgs[index])

        extraArgsValues = []
        for index in range(1, len(extraArgs), 2):
            extraArgsValues.append(extraArgs[index])

        self.extraArgs = dict(zip(extraArgsKeys, extraArgsValues))

        if (self.args.verbose > 0): #TODO: different log levels with -vv, etc.?
            logging.getLogger().setLevel(logging.DEBUG)

    #UserFunctor required method
    #Override this with your own workflow.
    def UserFunction(self, **kwargs):
        self.ParseArgs() #first, to enable debug and other such settings.
        self.RegisterAllClasses()
        self.InitData()

    #RETURNS and instance of a Datum, UserFunctor, etc. which has been discovered by a prior call of RegisterAllClassesInDirectory()
    def GetRegistered(self, registeredName):
        registered = SelfRegistering(registeredName)
        if (not registered or not registered.IsValid()): #UserFunctors are Data, so everything should have an IsValid() method
            self.ExitDueToErr(f"{registeredName} not found.")
        return registered

