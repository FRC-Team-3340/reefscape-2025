import ntcore

class NetworkTable():
    inst = ntcore.NetworkTableInstance.getDefault()
    datatable = inst.getTable("datatable")
    
