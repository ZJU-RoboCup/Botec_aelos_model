import pybullet as p
import pybullet_data

class URDFModel:
    def __init__(self,name,*,realtime_sim = False):
        self.REALTIME_SIM = realtime_sim
        p.connect(p.GUI)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0,0,-9.8)
        p.setRealTimeSimulation(self.REALTIME_SIM)
        p.loadURDF("plane.urdf")
        urdf_file = "urdf/"+name
        startPos = [0,0,0.1]
        startOrientation = p.getQuaternionFromEuler([0,0,0])
        self._model = p.loadURDF(urdf_file,startPos,startOrientation)
        self._jointsInfo = []
        self._jointsUserDebugParam = []
        for i in range(p.getNumJoints(self._model)):
            info = p.getJointInfo(self._model, i)
            self._jointsInfo.append(info)
            print(i,info)

        self.CONTROL_JOINTS_NUM = min(100,p.getNumJoints(self._model))

        for i in range(self.CONTROL_JOINTS_NUM):
            jointName = self._jointsInfo[i][1]
            p.setJointMotorControl2(self._model, i, p.POSITION_CONTROL, targetVelocity=0, force=0)
            self._jointsUserDebugParam.append(p.addUserDebugParameter(str(jointName), self._jointsInfo[i][8], self._jointsInfo[i][9], (self._jointsInfo[i][8]+self._jointsInfo[i][9])/2))
            p.addUserDebugText(str(jointName),[0,0,0],parentObjectUniqueId=self._model,parentLinkIndex=i,textColorRGB=[1,0,0])
        pass

    def step(self):
        jointsParamRead = []
        for i in range(len(self._jointsUserDebugParam)):
            jointsParamRead.append(p.readUserDebugParameter(self._jointsUserDebugParam[i]))
        # print(jointsParamRead)

        for jointNum in range(self.CONTROL_JOINTS_NUM):
            p.setJointMotorControl2(self._model, jointNum, p.POSITION_CONTROL,targetPosition = jointsParamRead[jointNum])

        # for jointNum in range(CONTROL_JOINTS_NUM):
        res = p.getLinkState(self._model,0)
        gPos = res[0]
        gOri = res[1]
        if (not self.REALTIME_SIM):
            p.stepSimulation()
        
        return gPos+gOri
