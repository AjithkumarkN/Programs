from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException   
from datetime import date
from selenium.webdriver.common.action_chains import ActionChains
from pathlib import Path
import os
import csv
import zipfile
import xmltodict
import time
class tenant_And_Lispendens():
    options = Options()  
    options.add_argument("--headless") 
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    downloads_path = str(Path.home() / "Downloads")
    chrome_prefs = {"download.default_directory":downloads_path} 
    options.experimental_options["prefs"] = chrome_prefs
    s = Service(executable_path='/usr/bin/chromedriver')
    driver = webdriver.Chrome(service=s,options=options)
    clerk_url='https://ftp.duvalclerk.com/'
    driver.get(clerk_url)
    driver.implicitly_wait(2)
    driver.find_element(By.CSS_SELECTOR,'#user-box-text').send_keys('ftp_dualusername')
    driver.find_element(By.CSS_SELECTOR,'#pword-box-text').send_keys('ftp_dualpassword')
    driver.find_element(By.CSS_SELECTOR,'#btn-LoginButton').click()
    click_action=ActionChains(driver)
    casefile_folder=driver.find_element(By.CSS_SELECTOR,'#ListFiles-row-0')
    click_action.double_click(casefile_folder).perform()
    time.sleep(2)
    file_location=driver.find_element(By.XPATH,"/html[1]/body[1]/div[55]/div[5]/span[1]/span[1]/span[1]/span[2]/span[1]/span[1]/span[2]/span[1]/span[last()-1]")
    click_action.double_click(file_location).perform()
    a=[]
    a.append(file_location.text.split('.'))
    filename=a[0][0]
    time.sleep(2)
    downloads_path = str(Path.home() / "Downloads")
    zip_path=os.path.join(downloads_path,filename+'.zip')
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(downloads_path)
    xml_path=os.path.join(downloads_path,filename+'.xml')
    xsd_path=os.path.join(downloads_path,filename+'.xsd')
    with open(xml_path, 'r') as xmlfile:
        xmlfiledata = xmlfile.read()
    xmlfiledata_dict = xmltodict.parse(xmlfiledata)
    petitionar_casedatas = [dict(x) for x in xmlfiledata_dict["Cases"]["Case"]]
    HEADERS = ['CaseID', 'Department', 'DivisionName', 'CaseTypeDescription', 'CaseNumber', 'FileDate']
    filerows = []
    for petitionar_casedata in petitionar_casedatas:
        CaseID = petitionar_casedata["CaseID"]
        Department= petitionar_casedata["Department"]
        DivisionName= petitionar_casedata["DivisionName"]
        CaseTypeDescription = petitionar_casedata["CaseTypeDescription"]
        CaseNumber= petitionar_casedata["CaseNumber"]
        FileDate= petitionar_casedata["FileDate"]
        filerows.append([CaseID,Department,DivisionName,CaseTypeDescription,CaseNumber,FileDate])
    csvfile_path=os.path.join(downloads_path,filename+'.csv')
    with open(csvfile_path, 'w',newline="") as csvfile_write:
        caseDetail_write = csv.writer(csvfile_write)
        caseDetail_write.writerow(HEADERS)
        caseDetail_write.writerows(filerows)
    today_dateTime = date.today()
    today_Date = today_dateTime.strftime("%Y-%m-%d")    
    convert_tenantfile=os.path.join(downloads_path,'tenent-'+today_Date+'.csv')
    convert_lispendensefile=os.path.join(downloads_path,'lispendence-'+today_Date+'.csv')
    court_url='https://core.duvalclerk.com/CoreCms.aspx'
    driver.get(court_url)
    driver.implicitly_wait(10)
    driver.find_element(By.CSS_SELECTOR,"input[name='ctl00$c_UsernameTextBox']").send_keys('dualcourt_username')
    driver.find_element(By.CSS_SELECTOR,"input[name='ctl00$c_PasswordTextBox']").send_keys('dualcourt_password')
    driver.find_element(By.CSS_SELECTOR,"input[value='Login to CORE']").click()
    teant_caseDtails=[]
    lispendense_caseDetails=[]
    def get_casenumber(self,csvfile_path):
        case_Details=[*csv.DictReader(open(csvfile_path))]
        for case_Detail in case_Details:
            case_Type=case_Detail['CaseTypeDescription'].upper()
            if 'EVICTION/DISTRESS FOR RENT' in case_Type:
                case_Number=case_Detail['CaseNumber']
                file_date_time=case_Detail['FileDate'].split('T')
                file_Date=file_date_time[0]
                obj.tenant_Lispendens_SearchCaseStatus(case_Number,file_Date,case_Type)
            elif 'FORECLOSURE' in case_Type:
                case_Number=case_Detail['CaseNumber']
                file_date_time=case_Detail['FileDate'].split('T')
                file_Date=file_date_time[0]
                obj.tenant_Lispendens_SearchCaseStatus(case_Number,file_Date,case_Type) 
    def tenant_Lispendens_SearchCaseStatus(self,case_Number,file_Date,case_Type):
        try:
            self.driver.find_element(By.CSS_SELECTOR,'body > form:nth-child(1) > div:nth-child(35) > div:nth-child(3) > div:nth-child(4) > div:nth-child(1) > div:nth-child(2) > div:nth-child(3) \
            > div:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(3) > td:nth-child(1) > input:nth-child(1)').send_keys(case_Number)
            self.driver.find_element(By.CSS_SELECTOR,'body > form:nth-child(1) > div:nth-child(35) > div:nth-child(3) > div:nth-child(4) > div:nth-child(1) > div:nth-child(2) > div:nth-child(3) \
            > div:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(4) > td:nth-child(1) > input:nth-child(1)').click()
            case_Id = self.driver.find_element(By.XPATH,("//span[@id='c_CaseNumberLabel']")).text
            case_Status = self.driver.find_element(By.XPATH,("//div[@class='caseDisplayTable caseSummary']/table/tbody/tr[2]/td[2]")).text
            if 'EVICTION/DISTRESS FOR RENT' in case_Type:
                if(file_Date==self.today_Date):    
                    if (case_Status=='OPEN'):
                            petitioner_Name = self.driver.find_element(By.XPATH,("//div[@class='caseDisplayTable']/table/tbody[2]/tr/td[1]")).text
                            party_type = self.driver.find_element(By.XPATH,("//div[@class='caseDisplayTable']/table/tbody[2]/tr/td[2]")).text
                            petitioner_Address = self.driver.find_element(By.XPATH,("//div[@class='caseDisplayTable']/table/tbody[2]/tr/td[3]")).text
                            tenant_CaseDetail= [
                                            {'Case_ID': case_Id, 'Case_Status': case_Status, 'Petitioner_Name': petitioner_Name, 'Party_Type':party_type, 'Address':petitioner_Address},
                                            ]
                            self.teant_caseDtails+=tenant_CaseDetail
                            self.driver.refresh()   
                    else:    
                        self.driver.refresh() 
                elif(case_Status=='OPEN'):
                    tenant_casestatus = [
                            {'Case_ID': case_Id, 'Case_Status': case_Status}, 
                                ]
                    self.teant_caseDtails+=tenant_casestatus
                    self.driver.refresh()
                else:
                    self.driver.refresh()            
            elif 'FORECLOSURE' in case_Type:        
                if (case_Status=='OPEN'):
                    lispendense_casestatus = [
                            {'Case_ID': case_Id, 'Case_Status': case_Status}, 
                                ]
                    self.lispendense_caseDetails+=lispendense_casestatus
                    self.driver.refresh()
                else:
                    self.driver.refresh()    
        except NoSuchElementException:
            self.driver.refresh()
        csv_Headings=['Case_ID','Case_Status','Petitioner_Name','Party_Type','Address']
        with open(self.convert_tenantfile, 'w', newline='') as tenant_outputfile:
            tenant_dict_writer = csv.DictWriter(tenant_outputfile, fieldnames=csv_Headings)
            tenant_dict_writer.writeheader()
            tenant_dict_writer.writerows(self.teant_caseDtails)
        with open(self.convert_lispendensefile, 'w', newline='') as lispendense_outputfile:
            lispendense_dict_writer = csv.DictWriter(lispendense_outputfile, fieldnames=csv_Headings)
            lispendense_dict_writer.writeheader()
            lispendense_dict_writer.writerows(self.lispendense_caseDetails)
obj=tenant_And_Lispendens()
obj.get_casenumber(obj.csvfile_path)
os.remove(obj.zip_path)
os.remove(obj.xml_path)
os.remove(obj.xsd_path)            
os.remove(obj.csvfile_path)
