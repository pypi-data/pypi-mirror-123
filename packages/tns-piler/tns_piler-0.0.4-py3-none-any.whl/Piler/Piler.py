import pysam, gffutils, csv, argparse
try:
    from Piler.pilerFunctions import *
except:
    from pilerFunctions import *


def main():

    parser = argparse.ArgumentParser(description="Make cumulative pileups")

    parser.add_argument("-d", "--dbLoc", help="Location of sql formatted annotation database", required=True)
    parser.add_argument("-t", "--transcript", help="Transcript to pile", required=True)
    parser.add_argument("-o", "--output", help="Output CSV location", required=True)
    parser.add_argument("files", nargs="+", help="Indexed, BAM files")

    args=parser.parse_args()

    db = gffutils.FeatureDB(args.dbLoc)

    transcriptBoundaries = list(getTranscriptExonBoundaries(args.transcript, db))

    out={}

    for bamfile in args.files:
        print("Piling...", bamfile)
        with pysam.AlignmentFile(bamfile, 'rb') as handledBAM:
            piles=[]

            for boundary in transcriptBoundaries:
                piles += getPiles(handledBAM, boundary)
            
            out[bamfile] = getCumulativePileups(piles, boundary[-1]) #strand
    

    with open(args.output, 'w') as outfile:
        outwriter=csv.writer(outfile)
        for key in out.keys():
            outwriter.writerow([key]+out[key])




if __name__=="__main__":
    main()