
class Part(object):

    def __str__(self):
        st = ""
        if hasattr(self, "name"):
            st += "name:" + self.name
        # HKT: This object doesn't have measures, perhaps this code was meant for the Node...
        # for stave in self.measures.keys():
        #     st += "\n"
        #     st += "Staff: "
        #     st += str(stave)
        #     st += "\n\r Details: \r"
        #     for key in self.measures[stave]:
        #         st += "Measure: "
        #         st += str(key)
        #         st += str(self.measures[stave][key])
        #     st += "\n--------------------------------------------------------"
        return st
