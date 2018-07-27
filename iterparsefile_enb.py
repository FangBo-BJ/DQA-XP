# Function: parse pm file (spm not include)
# v1.0,2018-7-14
# writen by FangBo

def iterparsefile_enb(filename,path,sn_file=0,city='bj',province='bj'):#core fun: parse the pm file
    lst_v = []
    lst_data = []
    dic_vlst = {}
    lst_colname = []
    lst_gcolname = []
    df =pd.DataFrame()
    isok = True
    sn = 1

    # Timer Start
    start_g = datetime.now()
    nbr_file = 0

    with gzip.open(filename,mode="r+b") as f:             
        tree = ET.iterparse(f)

        for event,elem in tree:               
            if elem.tag == "V":           
                # process each V
                lst_v.append(elem.text)
                lst_colname.append(elem.attrib['i'])
            elif elem.tag == "Measurements": # process each measurements           
                try:
                    df = pd.DataFrame(lst_data,columns=lst_gcolname)               
                except:
                    print('Construce DataFrame Error'+'\n')
                    print(filename)
                    isok = False
                    break

                df.rename(columns=dic_vlst,inplace=True)

                df.insert(0,'NBI_Ver',str_nbiversion)
                df.insert(0,'Vendor',str_vendorname)
                df.insert(0,'City',city)
                df.insert(0,'Province',province)
                df.insert(0,'ObjType',str_objtype)
                df.insert(0,'TimeInterval',timeinterval)
                df.insert(0,'startTime',str_begintime)

                df.to_csv(path+str_vendorname+'-'+str_objtype+'-'+'PM'+'-'+str(sn_file)+'-'+str(sn)+'.csv',index=False,encoding='gbk')
                sn+=1
                print(str_objtype)
                print(df.shape)
            elif elem.tag == "ObjectType":
                str_objtype = elem.text
                # initialize
                lst_data = []
                dic_vlst = {}               
                lst_v = []                                                                 
            elif elem.tag == "N":
                # process each N
                dic_vlst[elem.attrib["i"]] = elem.text
            elif elem.tag == "Pm":
                # add DN and Userlabel
                lst_v.insert(0,elem.attrib['Dn'])
                lst_v.insert(0,elem.attrib['UserLabel'])
                lst_colname.insert(0,'Dn')             
                lst_colname.insert(0,'UserLabel')

                lst_data.append(lst_v)
                lst_gcolname = lst_colname

                # reset
                lst_colname = []
                lst_v = []         
            elif elem.tag == "InfoModelReferenced":
                str_nbiversion = elem.text
            elif elem.tag == "VendorName":
                str_vendorname = elem.text
            elif elem.tag == "BeginTime":
                str_begintime = elem.text
            elif elem.tag =="InfoModelReferenced":
                str_infomodel = elem.text   
            elif elem.tag == "PmFile":
                #end parsing the file                   
                break               
            else:               
                continue
            elem.clear()
    # Timer Stop
    end_g = datetime.now()           
    print('Parsing File Time Using',end_g-start_g,'\n')

    return isok
