class IIO:
    element: str
    amount: float = 0
    minTemperature: float = 0
    radiation: float = 0
    diseaseId: str or None = None
    diseaseCount: float = 0

    def __init__(self):
        self.amount = 0
        self.minTemperature = 0
        self.radiation = 0
        self.diseaseId = None
        self.diseaseCount = 0

    def getSerializer(self):
        dict_iio = self.__dict__
        if self.diseaseId is None:
            del dict_iio['diseaseId']
            del dict_iio['diseaseCount']
        if self.radiation is None or self.radiation <= 0:
            del dict_iio['radiation']
        if self.minTemperature is None or self.minTemperature <= 0:
            del dict_iio['minTemperature']
        return dict_iio