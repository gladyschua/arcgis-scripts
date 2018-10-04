#--------------------------------------------------------------------------
# Tool Name:  Calculate proportion of attribute as fraction of its total
# Source Name: CalcProportion.py
#
# This script finds the proportion (of total) for a data field
# Input: Feature class layer
#        Field with data                   ! assumed numerical field
# Modify: Field for calculated proportion  ! assumed numerical field
#
#--------------------------------------------------------------------------
import sys, arcpy.da

try:
    infc = arcpy.GetParameterAsText(0)		        # Input feature class
    datafld = arcpy.GetParameterAsText(1)		# Input data field
    outfld = arcpy.GetParameterAsText(2)		# Modify result field
except:
    arcpy.AddError("Cannot parse input arguments")
    sys.exit("Error reading arguments!")

arcpy.AddMessage("Computing proportions...")

try:
   # instantiate variable
    total = 0.0

   # open as read only - read features and total data_value
    with arcpy.da.SearchCursor(infc, [datafld]) as rows:
        for row in rows:
            if row[0] is not None:
                   total += row[0]
       
   # open as read/write - read features again and calc proportion = data_value/total
    with arcpy.da.UpdateCursor(infc, [datafld,outfld]) as rows:
        for row in rows:
            if row[0] is not None:
                    row[1] = row[0]/total
            rows.updateRow(row)
    
    arcpy.SetParameterAsText(3,infc)		# Set feature layer as output to support data flows
    arcpy.AddMessage("Completed")

except:
    errMsg = arcpy.GetMessages(2)
    arcpy.AddError("Unexpected error : " + errMsg)
