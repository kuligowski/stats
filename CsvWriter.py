class CsvWriter:

    async def writeToCSV(self, data, fileName):
        print('writing to ' + fileName)
        try:
            data.to_csv(fileName + '.csv')
        except Exception as e:
            print(e)
            return -1
