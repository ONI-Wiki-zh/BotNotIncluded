# 配方

class Recipe:
    fabricator: str
    input = []
    output = []
    workTime: int = 1

    @staticmethod
    def getRecipeSerializer(fabricator, input, output, worktime):
        mSelf = Recipe()
        mSelf.fabricator = fabricator
        mSelf.input = input
        mSelf.output = output
        mSelf.workTime = worktime
        return mSelf.__dict__

    def getSerializer(self):
        return self.__dict__
