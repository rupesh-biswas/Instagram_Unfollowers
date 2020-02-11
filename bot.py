from time import sleep
from selenium import webdriver
import sys
import pandas as pd

class InstaBot:
    def __init__(self,usrname,psswrd):
        self.usrname=usrname
        self.psswrd=psswrd
        self.driver= webdriver.Chrome()
        self.driver.get('https://instagram.com')
        sleep(2)
        self.driver.find_element_by_xpath("//a[contains(text(), 'Log in')]").click()
        sleep(2)
        login_field=self.driver.find_element_by_xpath("//input[@name=\"username\"]")
        login_field.send_keys(usrname)
        psswrd_field=self.driver.find_element_by_xpath("//input[@name=\"password\"]")
        psswrd_field.send_keys(psswrd)
        self.driver.find_element_by_xpath('//button[@type="submit"]').click()
        sleep(5)
        self.driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]") \
            .click()
        sleep(2)

    def get_unfollowers(self):
        self.driver.find_element_by_xpath(f"//a[contains(@href, '/{self.usrname}')]") \
            .click()
        sleep(2)
        self.driver.find_element_by_xpath(f"//a[contains(@href, '/following')]") \
            .click() 
        following = self._get_names()
        self.driver.find_element_by_xpath(f"//a[contains(@href, '/followers')]") \
            .click()
        followers = self._get_names()

        not_following_back = [user for user in following if user not in followers]
        return not_following_back

    def _get_names(self):
        sleep(2)
        scroll_box=self.driver.find_element_by_xpath("/html/body/div[4]/div/div[2]")
        last_ht, ht = 0, 1
        while last_ht != ht:
            last_ht = ht
            sleep(2)
            ht = self.driver.execute_script("""
                arguments[0].scrollTo(0, arguments[0].scrollHeight);
                return arguments[0].scrollHeight;
                """, scroll_box)

        links = self.driver.find_elements_by_tag_name('a')
        names = [name.text for name in links if name != '']
        #close_buton
        self.driver.find_element_by_xpath("/html/body/div[4]/div/div[1]/div/div[2]/button") \
            .click()
        return names


if __name__=="__main__":
    usrname = sys.argv[1]
    psswrd =  sys.argv[2]
    my_bot=InstaBot(usrname,psswrd)
    unfollowers=my_bot.get_unfollowers()
    print(unfollowers)
    df=pd.DataFrame(unfollowers, columns=['unfollowers'])
    df=df.drop([0,1])
    df=df.reset_index(drop=True)
    df.to_csv('unfollowers.csv')