import fnmatch,os,glob,httplib,urllib

# constants
PATHTOBUILD = '/path/to/files/you/wanna/build'
EXCLUDEDIRS = ['fonts','ico','img','lib']

# recursively loop through files in sidekick-built
for root, dirnames, filenames in os.walk(PATHTOBUILD):
    
    # exclude specific folders
    for exfolder in EXCLUDEDIRS:
        if exfolder in dirnames:
            dirnames.remove(exfolder)
        
    # Uglify js files by sending to service
    for filename in fnmatch.filter(filenames, '*.js'):
        filepath = os.path.join(root, filename)
        
        # open file for reading
        fr = open(filepath,'r')
        
        # read into string
        jscode = fr.read()
        fr.close()
        
        # set up params and headers
        params = urllib.urlencode({'js_code': jscode})
        headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
        httpcon = httplib.HTTPConnection("marijnhaverbeke.nl")
        httpcon.request("POST", "/uglifyjs", params, headers)
        
        # get response
        response = httpcon.getresponse()
        
        # open file for writing
        data = response.read()
        fw = open(filepath,'w')
        
        # overwrite contents with uglified js
        fw.write(data)

        # close file and connection
        fw.close()
        httpcon.close()

    # Minify css files by sending to service
    for filename in fnmatch.filter(filenames, '*.css'):
        filepath = os.path.join(root, filename)
        
        # open file for reading
        fr = open(filepath,'r')
        
        # read into string
        csscode = fr.read()
        fr.close()
        
        # set up params and headers
        params = urllib.urlencode({'input': csscode})
        headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
        httpcon = httplib.HTTPConnection("www.cssminifier.com")
        httpcon.request("POST", "/raw", params, headers)
        
        # get response
        response = httpcon.getresponse()
        
        # open file for writing
        data = response.read()
        fw = open(filepath,'w')
        
        # overwrite contents with minified css
        fw.write(data)

        # close file and connection
        fw.close()
        httpcon.close()

    # minify html files by removing linebreaks
    for filename in fnmatch.filter(filenames, '*.html'):
        filepath = os.path.join(root, filename)
        
        # open file for reading
        fr = open(filepath,'r')

        # loop through lines, build array
        line_list = []
        for line in fr:
            line_list.append(line.rstrip('\r\n'))

        # close file
        fr.close()
        
        # concatenate lines into string
        smallhtml = ''.join(line_list)

        # overwrite contents of file with minified html
        fw = open(filepath,'w')
        fw.write(smallhtml)

        # close file
        fw.close()
