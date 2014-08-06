# ****************************************
# *                                      *
# *       ACCURANCY CHECKS & STATS       *
# *                                      *
# ****************************************

print """
**************************************
*   TOTAL ROOMS & CAPACITY CHECKS    *
**************************************
"""

print "There are " + str(len(allRooms)) + " total rooms."

numberOfDoubles = 0
numberOfSingles = 0
for room in allRooms:
    if room.capacity == 'Double':
        numberOfDoubles += 1
    if room.capacity == 'Single':
        numberOfSingles += 1
print "There are " + str(numberOfDoubles) + " doubles and " + str(numberOfSingles) + " singles."
print "This adds up to " + str((2 * numberOfDoubles) + numberOfSingles) + " residents."

print """
**************************************
*         GRT SECTION CHECKS         *
**************************************
"""

totalResidentsAccountFor = 0
for section in allSections:
    numberOfSinglesInSection = 0
    numberOfDoublesInSection = 0
    for entry in section.rooms:
        room = find(entry)
        if str(room.capacity) == 'Single':
            numberOfSinglesInSection += 1
        elif str(room.capacity) == 'Double':
            numberOfDoublesInSection += 1
    totalResidentsAccountFor += numberOfSinglesInSection + (2 * numberOfDoublesInSection)
    print "GRT Section " + str(section.label).rjust(5) + " has " + str(len(section.rooms)) + " rooms (" + "%02d" % (numberOfSinglesInSection,) + " singles and " + "%02d" % (numberOfSinglesInSection,) + " doubles = " + str(numberOfSinglesInSection + (2 * numberOfDoublesInSection)) + " residents)."
print str(totalResidentsAccountFor) + " residents are assigned to sections."

print """
**************************************
*       SQUARE FOOTAGE CHECKS        *
**************************************
"""

numberOfSizelessRooms = 0
for room in allRooms:
    if str(room.size) == None:
        numberOfSizelessRooms += 1
print str(numberOfSizelessRooms) + " rooms are missing square footage data."

sizeOfLargestSingle = 0
sizeOfSmallestSingle = 1000
sizeOfLargestDouble = 0
sizeOfSmallestDouble = 1000

totalAreaOfSingles = 0
totalAreaOfDoubles = 0

for room in allRooms:
    if str(room.capacity) == 'Single':
        totalAreaOfSingles += int(room.size)
        sizeOfLargestSingle = max(int(room.size), sizeOfLargestSingle)
        sizeOfSmallestSingle = min(int(room.size), sizeOfSmallestSingle)  
    elif str(room.capacity) == 'Double':
        totalAreaOfDoubles += int(room.size)
        sizeOfLargestDouble = max(int(room.size), sizeOfLargestDouble)
        sizeOfSmallestDouble = min(int(room.size), sizeOfSmallestDouble)

averageSizeOfSingle = totalAreaOfSingles / numberOfSingles
averageSizeOfDouble = totalAreaOfDoubles / numberOfDoubles

print "Singles range in size from " + str(sizeOfSmallestSingle) + " sq ft to " + str(sizeOfLargestSingle) + " sq ft, averaging " + str(averageSizeOfSingle) + " sq ft."
print "Doubles range in size from " + str(sizeOfSmallestDouble) + " sq ft to " + str(sizeOfLargestDouble) + " sq ft, averaging " + str(averageSizeOfDouble) + " sq ft."

print """
**************************************
*    BOSTON/CAMBRIDGE SIDE CHECKS    *
**************************************
"""

numberOfViewlessRooms = 0
numberOfCambridgeSideRooms = 0
numberOfBostonSideRooms = 0

for room in allRooms:
    if room.view == 'Boston':
        numberOfBostonSideRooms += 1
    elif room.view == 'Cambridge':
        numberOfCambridgeSideRooms += 1
    elif room.view == None:
        numberOfViewlessRooms += 1

print str(numberOfViewlessRooms) + " rooms are missing view data."
print str(numberOfBostonSideRooms) + " rooms face Boston, " + str(numberOfCambridgeSideRooms) + " rooms face Cambridge."

print """
**************************************
*           POSITION CHECKS          *
**************************************
"""

numberOfRoomsWithNoPositionData = 0
for room in allRooms:
    if str(room.X) == None or str(room.Y) == None:
        numberOfRoomsWithNoPositionData += 1
        print str(room.num) + " is missing position data."
print str(numberOfRoomsWithNoPositionData) + " rooms are missing position data."

for room in allRooms:
    if room.Y % 3 != 0:
        print room.num + " has incorrect vertical position."


print """
**************************************
*        HAS CURVY WALL CHECKS       *
**************************************
"""

print str(len(listOfMinorCurvyWalls) + len(listOfMajorCurvyWalls) + len(listOfAwfulCurvyWalls)) + " rooms have curvy walls, " + str(len(listOfMinorCurvyWalls)) + " minor, " + str(len(listOfMajorCurvyWalls)) + " major, " + str(len(listOfAwfulCurvyWalls)) + " awful."


print """
**************************************
*           BATHROOM CHECKS          *
**************************************
"""

for room in allRooms:
    if room.bathroom == None:
        print room.num + " has no bathroom."

numberOfResidentsWithBathrooms = 0
numberOfRoomsWithBathrooms = 0
for room in allRooms:
    if room.bathroom != None:
        numberOfRoomsWithBathrooms += 1
        if room.capacity == 'Single':
            numberOfResidentsWithBathrooms += 1
        elif room.capacity == 'Double':
            numberOfResidentsWithBathrooms += 2
        else:
            raise "Hell!"

print "There are " + str(len(allBathrooms)) + " total bathrooms, with an average of " + str( numberOfResidentsWithBathrooms / float(len(allBathrooms)) ) +  " users each." 

numInternal = 0
numInsuite = 0
numHallway = 0
for bathroom in allBathrooms:
    if bathroom.location == 'internal':
        numInternal += 1
    if bathroom.location == 'insuite':
        numInsuite += 1
    if bathroom.location == 'hallway':
        numHallway += 1

print "There are " + str(numInternal) + " internal bathrooms, " + str(numInsuite) + " insuite bathrooms, and " + str(numHallway) + " hallway bathrooms."

print str(numberOfRoomsWithBathrooms) + " rooms (" + str(numberOfResidentsWithBathrooms) + " residents)" + " have assigned bathrooms."

numberOfSinglesWithExclusiveBathrooms = 0
numberOfDoublesWithExclusiveBathrooms = 0
numberOfSinglesWithInternalBathrooms = 0
numberOfDoublesWithInternalBathrooms = 0
for room in allRooms:
    if room.capacity == 'Single':
        bath = findBathroom(room.bathroom)
        sharedWith = bath.rooms
        if bath.location == 'internal':
            numberOfSinglesWithInternalBathrooms += 1
            numberOfSinglesWithExclusiveBathrooms += 1
        elif len(sharedWith) == 1:
            numberOfSinglesWithExclusiveBathrooms += 1
    if room.capacity == 'Double':
        bath = findBathroom(room.bathroom)
        sharedWith = bath.rooms
        if bath.location == 'internal':
            numberOfDoublesWithInternalBathrooms += 1
            numberOfDoublesWithExclusiveBathrooms += 1
        elif len(sharedWith) == 1:
            numberOfDoublesWithExclusiveBathrooms += 1

print "There are " + str(numberOfSinglesWithExclusiveBathrooms) + " singles with their own bathoom, of which " + str(numberOfSinglesWithInternalBathrooms) + " are internal."
print "There are " + str(numberOfDoublesWithExclusiveBathrooms) + " doubles with their own bathoom, of which " + str(numberOfDoublesWithInternalBathrooms) + " are internal."

print "Checks completed."

