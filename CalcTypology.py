#--------------------------------------------------------------------------
# Tool Name: CalcTypology
# Description: Classifies regions as 'Urban', 'Intermediate' or 'Rural'
#              by urban population share for regions and urban population
# Input: Region feature class layer
#       Region population field             !assumed numerical field
#       Region urban population field       !assumed numerical field
# Modify: Field for typology                !assumed text field
#
#--------------------------------------------------------------------------
import sys, arcpy.da

try:
    infc = arcpy.GetParameterAsText(0)		        # Input feature class
    datafld_regPop = arcpy.GetParameterAsText(1)	# Input data field - Region population
    datafld_regUrbanPop = arcpy.GetParameterAsText(2)	# Input data field - Region urban population
    outfld = arcpy.GetParameterAsText(3)	        # Modify result field
except:
    arcpy.AddError("Cannot parse input arguments")
    sys.exit("Error reading arguments!")

arcpy.AddMessage("Computing typology...")

try:
    # instantiate variable
    urbanPopShare = 0.0
       
    # use UpdateCursor to open as read/write
    # wrapping the cursor in a WITH statement,
    # opens and closes the row and cursor objects at the end of the code block
    with arcpy.da.UpdateCursor(infc, ['Population', 'Urban_Pop', outfld]) as rows:
        for row in rows:
            
            # check value is not null
            if (row[0] is None or row[1] is None):
                row[2] = None
                rows.updateRow(row)
                
            # check value is not negative  
            if (row[0] > 0 and row[1] > 0):
                # compute the urban population share ratio as Urban_Pop/Population
                urbanPopShare = row[1]/row[0]
                
                # check share ratio >= 0.5
                if urbanPopShare >= 0.5:
                    # check Urban Population
                    if row[1] < 500000:
                        # if Urban Population < 500 000
                        row[2] = 'Intermediate'
                        rows.updateRow(row)
                    else:
                        # if Urban Population > 500 000
                        row[2] = 'Urban'
                        rows.updateRow(row)
                        
                # check share ratio < 0.5 AND share ratio >= 0.15
                elif (urbanPopShare < 0.5 and urbanPopShare >= 0.15):
                    
                    if row[1] < 500000:
                        # if Urban Population < 500 000
                        row[2] = 'Rural'
                        rows.updateRow(row)
                        
                    else:
                        # if Urban Population > 500 000
                        row[2] = 'Intermediate'
                        rows.updateRow(row)
                        
                # check share ratio < 0.15
                else:
                    row[2] = 'Rural'
                    rows.updateRow(row)
            # when value is negative or out of range 
            else:
                row[2] = None
                rows.updateRow(row)

    arcpy.SetParameterAsText(4,infc)		# Set feature layer as output to support data flows
    arcpy.AddMessage("Completed")

except:
    errMsg = arcpy.GetMessages(2)
    arcpy.AddError("Unexpected error : " + errMsg)
