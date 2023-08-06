from pybtex.database import parse_file, BibliographyData, Entry
import sys, click, os
from thefuzz import fuzz

bibpath=os.environ['HOME']+"/.biblib.bib"

types=["article","book","booklet","conference","inbook","incollection","inproceedings","manual","mastersthesis","misc","phdthesis","proceedings","techreport","unpublished"]
fields=["abstract","tags","label","address","annotate","author","booktitle","chapter","crossref","edition","editor","howpublished","institution","journal","key","month","note","number","organization","pages","publisher","school","series","title","type","volume","year","doi"]
required=["title","author","year","label","type"]


def kwargstotups(kwargs):
    return [(key, kwargs[key]) for key in kwargs.keys() if key!="type"]

def confinput(message):
    inp=input(message)
    conf=False
    while conf!=True:
        conf=boolinput("Are you sure [bool]?")
        if conf!=True:
            inp=input(message)
    return inp

def boolinput(message):
    choice="yeet"
    while choice not in [True,False]:
        choice=input(message)
        if choice.lower() in ["true","1","y","yes"]:
            choice=True
        elif choice.lower() in ["false","0","n","no"]:
            choice=False
        first=False
    return choice

def check_req(kwargs):
    return [r for r in required if kwargs[r]==None]

def choice_menu(choices):
    if len(choices)>1:
        choice=None
        while type(choice)!=int or not 0<=choice<=len(choices)-1:

            for ind,val in enumerate(choices):
                print(ind,") ",val)

            choice=input("Which [0 to %s]? "%(len(choices)-1))
            if choice.isdigit():
                choice=int(choice)
            first=False
        return choice
    else:
        return 0

def append(file,bib):
        with open(file,"a+") as f:
            f.write("\n"+bib.to_string("bibtex"))

def prestart():
    if not os.path.exists(bibpath):
        print("Initialising biblib")
        with open(bibpath,"w") as f:
            f.write("%Bibliography database for biblib command line tool\nThis is automatically generated so edit at your own (fairly inconsequential) risk")
    return 0

def searchbib(**kwargs):
    bib=parse_file(bibpath)
    outbib=""
    if type(kwargs["sensetivity"])!=int:
        if kwargs["sensetivity"].isdigit()==True:
            kwargs["sensetivity"]=int(kwargs["sensetivity"])
        else:
            kwargs["sensetivity"]=80

    for entry in bib.entries:
        if kwargs["tags"]!=None and len([tag for tag in kwargs["tags"].split(",") if tag in bib.entries[entry].fields["tags"].split(",")]):
            outbib+=bib.entries[entry].to_string("bibtex")
        elif kwargs["search"]!=None and fuzz.partial_ratio(kwargs["search"],bib.entries[entry].to_string("bibtex"))>=kwargs["sensetivity"]:
            outbib+=bib.entries[entry].to_string("bibtex")
        else:
            pass
    if kwargs["tags"]==None and kwargs["search"]==None:
        outbib=bib.to_string("bibtex")

    return outbib

@click.group()
@click.version_option("0.0.1")
def main():
    prestart()

@main.command()
@click.help_option('-h', '--help')
#these were programatically generated because click doesn't let you put lots in at once
@click.option('--address','address',required=False)
@click.option('--abstract','abstract',required=False)
@click.option('--annotate','annotate',required=False)
@click.option('--author','author',required=False)
@click.option('--booktitle','booktitle',required=False)
@click.option('--chapter','chapter',required=False)
@click.option('--crossref','crossref',required=False)
@click.option('--edition','edition',required=False)
@click.option('--editor','editor',required=False)
@click.option('--howpublished','howpublished',required=False)
@click.option('--institution','institution',required=False)
@click.option('--journal','journal',required=False)
@click.option('--key','key',required=False)
@click.option('--month','month',required=False)
@click.option('--note','note',required=False)
@click.option('--number','number',required=False)
@click.option('--organization','organization',required=False)
@click.option('--pages','pages',required=False)
@click.option('--publisher','publisher',required=False)
@click.option('--school','school',required=False)
@click.option('--series','series',required=False)
@click.option('--title','title',required=False)
@click.option('--type','type',required=False)
@click.option('--volume','volume',required=False)
@click.option('--year','year',required=False)
@click.option('--doi','doi',required=False,help="doi")
@click.option('--tags','tags',required=False,help='tags for sorting bibliography, commer delimited, be very careful to not include accidental spaces and to make them concistent (e.g. --tags "a,b,c" is not the same as --tags "a, b, c")')
@click.option('--label','label',required=False,help="short identifier, will be used as latex label (i.e. \cite{label})")
@click.option('--force',default=False,help="when force is set to true won't ask for confirmation at any step")
def add(**kwargs):
    """Add an entry to the bibliography, supply options or run with none for an interactive input\nUnless otherwise specified parameters are bibtex parameters and more info is available at https://www.openoffice.org/bibliographic/bibtex-defs.pdf"""
    still_req=check_req(kwargs)
    if len(still_req)>0:
        print("You have not entered: %s"%", ".join(still_req))
    while len(still_req)!=0:
        choice=choice_menu(still_req)
        kwargs[still_req[choice]]=input("%s: "%still_req[choice])
        still_req.remove(still_req[choice])

    existingbib=parse_file(bibpath)
    while kwargs["label"] in existingbib.entries:
        kwargs["label"]=confinput("You have entered a label clashing with an existing entry (%s), please enter a new one (you may have already entered this article): "%kwargs["label"])

    if kwargs["force"] == False:
        more=boolinput("Would you like to add anymore fields [bool]? ")

    entered=[val for val in fields if kwargs[val]!=None]

    while kwargs["force"] == False and more==True and len(entered)!=len(fields):
        rem=[f for f in fields if f not in entered]
        choice=choice_menu(rem)
        kwargs[rem[choice]]=confinput("%s: "%rem[choice])
        more=boolinput("Would you like to add anymore fields [bool]? ")

    if kwargs["force"] == False:
        print("You have entered:")
        for key in kwargs.keys():
            if kwargs[key]!=None and key!="force":
                print("    %s: %s"%(key,kwargs[key]))
        conf=boolinput("Is this correct [bool]?")

    while kwargs["force"] == False and conf!=True:
        print("Which do you want to edit?")
        choice=choice_menu(fields)
        kwargs[fields[choice]]=confinput("%s: "%fields[choice])
        conf=not boolinput("Would you like to edit anymore fields [bool]? ")

    while kwargs["type"] not in types:
        print("You have not entered a valid type, the choices are:")
        choice=choice_menu(types)
        kwargs["type"]=types[choice]

    bib=BibliographyData({kwargs["label"]:Entry(kwargs["type"], [(key, kwargs[key]) for key in kwargs.keys() if key not in ["type","label","force"] and kwargs[key]!=None])})

    append(bibpath,bib)

    return 0

@main.command()
@click.option('--tags','tags',required=False,help="tags to search for, see add for details")
@click.option('--search','search',required=False,help="terms to search entries for")
@click.option('--sensetivity','sensetivity',default=80,required=False,help="sensetivity of fuzzy search, defaults to 80% (80)")
@click.option('--bibtex',default="False",required=False,help="output bibtex file, forces true if compile is true, defaults to false")
@click.option('--compile',default="False",required=False,help="compile output to pdf, defaults to false")
@click.option('--stdout',default="True",required=False,help="output bibliography to command line, defaults to true")
def show(**kwargs):
    """Display and output bibliography"""
    outbib=searchbib(**kwargs)
    if kwargs["bibtex"].lower() in ["true","1","y","yes"] or kwargs["compile"].lower() in ["true","1","y","yes"]:
        with open("output.bib","w") as f:
            f.write(outbib)   

    if kwargs["compile"].lower() in ["true","1","y","yes"]:
        with open("bibliography.tex","w") as f:
            f.write("""\\documentclass[letterpaper,11pt]{article}
\\usepackage[backend=bibtex,style=nature]{biblatex}
\\bibliography{output} 

\\begin{document}
\\nocite{*}
\\printbibliography
\\end{document}""")
        print("This currently doesn't work so outputs a bib file and a tex file for you to compile")
        #print("This is going to show you ~~errors~~, just keep pressing enter, they are actually warnings that are wrong and I don't know how to supress")
        #os.system("pdflatex -pdf bibliography.tex; "#+"; ".join(["rm %s"%x for x in ["*.aux", "*.blg", "*.dvi", "*.fls", "*synctex.gz", "*.bbl", "*-blx.bib", "*.fdb_latexmk", "*.log", "*.run.xml", "output.bib","bibliography.tex"]]))

    if kwargs["stdout"].lower() in ["true","1","y","yes"]:
        print(outbib)
    return 0

if __name__=="__main__":
    args=sys.argv
    prestart()
    main()