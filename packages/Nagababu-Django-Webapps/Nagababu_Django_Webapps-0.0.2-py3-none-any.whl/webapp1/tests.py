import unittest
import HtmlTestRunner
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from django.contrib.auth.models import  User
from .forms import  CustRegiForm,Login_form, Project_form,update_profile
from .models import *

from django.test import TestCase


#   ***************************************************************************************************
#   *                                FUNCTIONAL                                                       *
#   *                                          TESTING                                                *
#   ***************************************************************************************************



class FunctionalTests(TestCase):
    @classmethod
    def setUp(cls):
        cls.driver = webdriver.Chrome("H://chromedriver.exe")
        cls.driver.implicitly_wait(10)
        cls.driver.maximize_window()

    def test1(self):  # This is for registration

        self.driver.get('http://127.0.0.1:8000/food/Registration/')
        time.sleep(10)
        username=self.driver.find_element_by_xpath("//input[@name='username']")
        username.send_keys('Testuser1',Keys.ARROW_DOWN)
        time.sleep(10)
        email=self.driver.find_element_by_xpath("//input[@name='email']")
        email.send_keys("testcase@gmail.com",Keys.ARROW_DOWN)
        time.sleep(10)
        mobile=self.driver.find_element_by_xpath("//input[@name='mobile']")
        mobile.send_keys("8787865674",Keys.ARROW_DOWN)
        time.sleep(10)
        password1=self.driver.find_element_by_xpath("//input[@name='password1']")
        password1.send_keys("Test@sample123",Keys.ARROW_DOWN)
        time.sleep(10)
        password2 = self.driver.find_element_by_xpath("//input[@name='password2']")
        password2.send_keys("Test@sample123",Keys.ARROW_DOWN)
        time.sleep(10)
        btn=self.driver.find_element_by_xpath("//input[@name='reg_sign']")
        btn.submit()

    def test2(self):
        self.driver.get("http://127.0.0.1:8000/food/Login/")
        time.sleep(5)
        email=self.driver.find_element_by_xpath("//input[@name='Email']")
        email.send_keys("nagababuupputuri52@gmail.com",Keys.ARROW_DOWN)
        time.sleep(5)
        password=self.driver.find_element_by_xpath("//input[@name='password']")
        password.send_keys("Jeevan$123",Keys.ARROW_DOWN)
        time.sleep(3)
        l_btn=self.driver.find_element_by_xpath("//button[@name='log_button']")
        l_btn.submit()
    def test3(self): # This is the home_nav
        self.driver.get("http://127.0.0.1:8000/")
        time.sleep(5)
        self.driver.find_element_by_link_text("Register").click()
    def test4(self):
        self.driver.get("http://127.0.0.1:8000/")
        self.driver.find_element_by_link_text("Login").click()
        time.sleep(3)
    def test5(self):
        self.driver.get("http://127.0.0.1:8000/")
        self.driver.find_element_by_link_text("Admin").click()
        time.sleep(3)
    # def test6(self):
    #     self.driver.get("http://127.0.0.1:8000/")
    #     self.driver.find_element_by_link_text("").click()
    #     time.sleep(3)

    def test6(self):
        self.driver.get("http://127.0.0.1:8000/")
        time.sleep(3)
        self.driver.find_element_by_name("item_home").click()
    def test7(self):
        self.driver.get("http://127.0.0.1:8000/")
        self.assertIn("Django",self.driver.page_source)

    def test8(self):
        self.driver.get("http://127.0.0.1:8000/food/Login/")
        self.driver.find_element_by_name("for_pwd").click()


    def test9(self):  # This is for Forget Password
        self.driver.get("http://127.0.0.1:8000/food/password_reset/")
        time.sleep(2)
        for_email=self.driver.find_element_by_name("email")
        for_email.send_keys("sample@gmail.com",Keys.ARROW_DOWN)

        self.driver.find_element_by_name("re_my_pwd").click()


    def test10(self): #submit idea
        self.driver.get("http://127.0.0.1:8000/food/Project/")
        time.sleep(5)
        idea_title=self.driver.find_element_by_name("pro_form_title")
        idea_title.send_keys("This is sample idea",Keys.ARROW_DOWN)
        time.sleep(5)
        idea_email=self.driver.find_element_by_name("Project_Email")
        idea_email.send_keys("nagababuupputuri52@gmail.com",Keys.ARROW_DOWN)
        time.sleep(5)
        idea_desc=self.driver.find_element_by_name("Project_Email")
        idea_desc.send_keys("This is sample project desc for automation testing ",Keys.ARROW_DOWN)
        time.sleep(5)
        pro_btn=self.driver.find_element_by_name("idea_sub").submit()
        time.sleep(10)
    @classmethod
    def tearDown(cls):
        cls.driver.close()
        cls.driver.quit()

#   ***************************************************************************************************
#   *                                UNIT                                                             *
#   *                                    TESTING                                                      *
#   ***************************************************************************************************
class UnitTestCase(TestCase):


    def test_home_homepage_tempalte(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'webapp1/home.html')

    #check if the registration form is valid/not
    def test_registration_form(self):
        #This form in not a valid because password similar to username
        # form = CustRegiForm(data={'username': 'backenduser',"email":"backend@gmail.com","mobile":"8716272211",
        #                           "password1":"backend@123","password2":"backend@123"})
        form = CustRegiForm(data={'username': 'backenduser',"email":"backend@gmail.com",
                                   "password1":"check@123","password2":"check@123"})
        self.assertTrue(form.is_valid())

    def test_login_form(self):
        form=Login_form(data={"Email":"nagababuupputuri52@gmail.com","password":"Jeevan$123"})
        self.assertTrue(form.is_valid())

    def test_project_form(self):
        form=Project_form(data={"pro_form_title":"This is testing in backend","Project_Email":"nagababuupputuri52@gmail.com",
                                "Project_Description":"Hi there , This project about testing a developed application"})
        self.assertTrue(form.is_valid())

    def test_update_profile_form(self):
        form=update_profile(data={"username":"Naga@123","Email":"nagababuupputuri12@gmail.com"})
        self.assertTrue(form.is_valid())

    #now save data into model
    def test_case_for_storing_data_into_reg_model(self):
        model=User()
        model.username="store_model_test_user"
        model.email="testcase_user@gmail.com"
        model.mobile="8821376785"
        model.password="Naga@123213"
        model.save()
        return model  # it returns the current saved user object
    def test_case_for_submit_idea(self):
        model=Project_Ideas()
        model.pro_title="This is Ai"
        model.pro_email="ai@gmail.com"
        model.pro_description="This is the sample description of ai"
        model.save()
        return model
if 'name'=="__main__":
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output="c:/data"))