from .devices import Hub, PC
from .process import CreateDevice, ConnectDevices,SendData,Disconnect
from .devices import Log
from app.interface_layer.parser_interface import ABCParser
from app.tools.file import  save


class PhysicalParser(ABCParser):
    def __init__(self):
        self.parsers = {"create": CreateParser(),
                        "connect":ConnectParser(),
                        "send":SendParser,
                        "disconnect":DisconnectParser
        }
    
    def save_data(self,file_name, devices):
        for d in devices:
            save(d+".txt","output/solution_"+file_name,devices[d].log.data)
        save("all.txt","output/solution_"+file_name,Log.all_data)
        print("Ok!")
    
class CreateParser():
    def __init__(self):
        self.device_parser = {"hub": self.hub,
                              "host": self.host 
        }
        self.device_class = {"hub": Hub,
                              "host":PC 
        }
        
    def execute(self, intruccion):
        device = intruccion.args.pop(0)
        values = None
        for key in self.device_parser:
            if device == key:
                values = self.device_parser[key](intruccion)
                break
        if not values is None:        
            return (values[0],CreateDevice(*values))  
       
    def hub(self,intruccion):
        return [intruccion.time, self.device_class['hub'], [intruccion.args[0], intruccion.args[1]]]  
    
    def host(self, intruccion):
        return [intruccion.time, self.device_class['host'], [intruccion.args[0]]]
     
class ConnectParser():
    def execute(self,intruccion):
        dev1, port1=intruccion.args.pop(0).split("_")
        dev2, port2=intruccion.args.pop(0).split("_")
        return (intruccion.time,ConnectDevices(intruccion.time,dev1, int(port1)-1,dev2, int(port2)-1 ))

class SendParser():
    def execute(intruccion):
        host = intruccion.args.pop(0)
        data = intruccion.args.pop(0)
        return (intruccion.time,SendData(intruccion.time,host, data))

class DisconnectParser:
    def execute(intruccion):
        dev1, port1=intruccion.args.pop(0).split("_")
        return (intruccion.time, Disconnect(intruccion.time,dev1, int(port1)-1))