from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

class Hosttest(TestCase):
    
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
        self.live_server_url = 'http://127.0.0.1:8000/'

    def tearDown(self):
        self.driver.quit()

    def test_02_login_page(self):
        driver = self.driver
        driver.get(self.live_server_url)
        driver.maximize_window()
        time.sleep(2)
        
        theme = driver.find_element(By.CSS_SELECTOR, "a#loginid")
        theme.click()
        time.sleep(1)
        
        elem = driver.find_element(By.NAME, "username")
        elem.send_keys("Fincity")
        elem = driver.find_element(By.NAME, "password")
        elem.send_keys("Fincity@12")
        
        submit_button = driver.find_element(By.CSS_SELECTOR, 'button#submit.btn.btn-primary.fw-bold[style*="background-color:#000000"]')
        submit_button.click()
        time.sleep(2)

        # Navigate to the "Create Profile" page
        browse = driver.find_element(By.CSS_SELECTOR, "li.has-sub > a.sidebar-link")
        browse.click()
        time.sleep(1)

        # Click on the "Post Job" link
        view = driver.find_element(By.CSS_SELECTOR, "a[href='/postjob']")
        view.click()
        time.sleep(1)

        # Fill in the form
        JobTitle = driver.find_element(By.CSS_SELECTOR, "input#JobTitle")
        JobTitle.send_keys("Android Developer")
        time.sleep(1)

        jobdescription = driver.find_element(By.CSS_SELECTOR, "textarea#jobdescription")
        jobdescription.send_keys("Android Developer post for freshers")
        time.sleep(1)

        # joblocation = driver.find_element(By.CSS_SELECTOR, "textarea#joblocation")
        # joblocation.send_keys("Kochi")
        # time.sleep(1)

        email = driver.find_element(By.CSS_SELECTOR, "input#emailid[type='email']")
        email.send_keys("fincity@gmail.com")
        time.sleep(1)

        jobtype = driver.find_element(By.CSS_SELECTOR, "select#basicSelect")
        select = Select(jobtype)
        select.select_by_value("Full Time")
        time.sleep(1)

        experience = driver.find_element(By.CSS_SELECTOR, "input#experience[type='number']")
        experience.send_keys("1")
        time.sleep(1)

        vaccancies = driver.find_element(By.CSS_SELECTOR, "input#vaccancies[type='number']")
        vaccancies.send_keys("1")
        time.sleep(1)

        date_input = driver.find_element(By.CSS_SELECTOR, "input#lastdate[type='date']")
        date_input.clear()
        date_input.send_keys('31-10-2023')
        time.sleep(2)

        # Submit the form
        postajob = driver.find_element(By.CSS_SELECTOR, "button#postajob")
        postajob.click()
        time.sleep(1)

        browse = driver.find_element(By.CSS_SELECTOR, "li.has-sub > a.sidebar-link")
        browse.click()
        time.sleep(1)

        # Click on the "Post Job" link
        view = driver.find_element(By.CSS_SELECTOR, "a[href='/managejobs/17/']")
        view.click()
        time.sleep(1)

    

        browse = driver.find_element(By.CSS_SELECTOR, "a.sidebar-link[href='/alljobsposted/']")
        browse.click()
        time.sleep(1)

        # Click on the "Post Job" link
        view = driver.find_element(By.CSS_SELECTOR, "a.btn.btn-success[href='/specificapplicant/34/']")
        view.click()
        time.sleep(1)
       
       
        
        view = driver.find_element(By.CSS_SELECTOR, 'a.btn.btn-success[href="/employeer/applicantdetails/9/13"]')
        view.click()
        time.sleep(1)

        view = driver.find_element(By.CSS_SELECTOR, 'a#interviewschedulingmodal.btn.btn.btn-warning.col-lg-4[data-toggle="modal"][data-target="#inlineForm"]')
        view.click()
        time.sleep(1)

        view = driver.find_element(By.CSS_SELECTOR, "button.close")
        view.click()
        time.sleep(1)

        
        view = driver.find_element(By.CSS_SELECTOR, "div.d-none.d-md-block.d-lg-inline-block")
        view.click()
        time.sleep(1)

        view = driver.find_element(By.CSS_SELECTOR, 'div.dropdown-menu.dropdown-menu-right.show a.dropdown-item')
        view.click()
        time.sleep(1)

        elem = driver.find_element(By.NAME, "username")
        elem.send_keys("Klaus")
        elem = driver.find_element(By.NAME, "password")
        elem.send_keys("Klaus@12")
        
        submit_button = driver.find_element(By.CSS_SELECTOR, 'button#submit.btn.btn-primary.fw-bold[style*="background-color:#000000"]')
        submit_button.click()
        time.sleep(2)
 
        view = driver.find_element(By.CSS_SELECTOR, 'a#loginid.btn.btn-light.fw-bold[href="/eligibility"]')
        view.click()
        time.sleep(1)

        view = driver.find_element(By.CSS_SELECTOR, 'input[type="checkbox"]#read-checkbox')
        view.click()
        time.sleep(1)

        view = driver.find_element(By.CSS_SELECTOR, "a#apply-btn.boxed-btn3.text-white.disabled")
        view.click()
        time.sleep(1)

        location_search = driver.find_element(By.CSS_SELECTOR, 'input#location_search[type="search"][placeholder="Search By Location"][name="location_searched"]')
        location_search.send_keys("Kochi")
        time.sleep(1)

        view = driver.find_element(By.CSS_SELECTOR, 'button#searchbtn.boxed-btn3.w-100[type="submit"]')
        view.click()
        time.sleep(1)

        view = driver.find_element(By.CSS_SELECTOR, 'a.boxed-btn3[href="/jobdetails/40"]')
        view.click()
        time.sleep(1)

        view = driver.find_element(By.CSS_SELECTOR, 'a[href="/candidate"]')
        view.click()
        time.sleep(1)

        view = driver.find_element(By.CSS_SELECTOR, 'a#loginid.btn.btn-light.fw-bold[href="/my_form"]')
        view.click()
        time.sleep(1)

        feedback = driver.find_element(By.CSS_SELECTOR, 'textarea.form-control[name="text1"][rows="10"][placeholder="Post your feedback here..."][required]')
        feedback.send_keys("Really Good")
        time.sleep(1)

        view = driver.find_element(By.CSS_SELECTOR, 'button.btn.btn-primary[type="submit"]')
        view.click()
        time.sleep(1)


