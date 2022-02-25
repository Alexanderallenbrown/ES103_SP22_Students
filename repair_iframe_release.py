import os
import shutil
import pwd
import argparse
import stat

import nbformat as nbf 


# badstring = '"https://alexanderallenbrown.github.io/es103_pulleysim/">'

badstring = '"https://alexanderallenbrown.github.io/es103_pulleysim/"<'


newsource = '''%%html
<iframe id="inlineFrameExample" title="Inline Frame Example" width="750" height="350" src="https://alexanderallenbrown.github.io/es103_pulleysim/index.html"></iframe>
'''


def set_permissions(path, uid, gid):
    os.chown(path, uid, gid)
    if os.path.isdir(path):
        os.chmod(path, stat.S_IRUSR | stat.S_IRGRP | stat.S_IXUSR | stat.S_IXGRP)
    else:
        os.chmod(path, stat.S_IRUSR | stat.S_IRGRP)


def main(name, student=None, force = False):
    working_dir = os.path.abspath(".")
    # update source directory
    src = os.path.join(working_dir, name)
    #we are replacing the notebook so destination and source are same
    dst = src

    # look for all notebooks in the submission directory
    for root, dirs, files in os.walk(src):
        for file in files:
            #the first version of this I made did a save-as with the prefix 'new.' remove this if it's still there.
            if(file[0:4]=="new_"):
               os.system("rm "+os.path.join(src,file))
               print("removing: "+os.path.join(src,file))
            elif file.endswith(".ipynb") and not "checkpoint" in file :
                #make a scrubbed version of the notebook
                cleannb = nbf.v4.new_notebook()
                #a variable to hold our new notebook's cells, one by one.
                cells = []
                ntbk = nbf.read(os.path.join(src,file), nbf.NO_CONVERT)
                cleannb.metadata = ntbk.metadata
                print("Scrubbing: "+os.path.join(src,file))
                for cell in ntbk.cells:       
                    #check to see if bad string is in this cell.
                    if badstring in cell.source:
                        print("BAD cell found. source: "+cell.source)
                        #now actually replace the bad string!
                        #cell.source = cell.source.replace(badstring,goodstring)
                        cell.source = newsource
                        print("new source: "+cell.source)

                        if "nbgrader" in cell.metadata:
                            del cell.metadata["nbgrader"]
                            print("deleted nbgrader metadata")
                        if "editable" in cell.metadata:
                            del cell.metadata["editable"]
                        if "deletable" in cell.metadata:
                            del cell.metadata["deletable"]
                        if "hide_input" in cell.metadata:
                            cell.metadata["hide_input"]="false"
                        print(cell.metadata)
                    cells.append(cell)
                #add our cells to the new notebook object
                cleannb['cells'].extend(cells)

                #write the resource notebook to a file
                nbf.write(cleannb,os.path.join(dst,file))
                #change permissions
#                     os.system("chmod 777 -R "+dst)
                #change ownership
#                     os.system("chown root:ES103_instructors "+os.path.join(dst,file))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('name', help='the name of the assignment')
    parser.add_argument('--student', default=None, help='the name of a specific student')
    parser.add_argument('--force', action="store_true", default=False,
                        help='overwrite existing feedback (use with extreme caution!!)')

    args = parser.parse_args()
    main(args.name, student=args.student, force=args.force)
