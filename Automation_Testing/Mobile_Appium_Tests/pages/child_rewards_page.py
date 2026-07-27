from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage

class ChildRewardsPage(BasePage):
    """Page Object for ChildRewardsActivity."""

    TV_TOTAL_POINTS = (AppiumBy.ID, "com.example.smileapp:id/tvRewardsTotalPoints")
    BTN_REDEEM_TEDDY = (AppiumBy.ID, "com.example.smileapp:id/btnRedeemTeddy")
    BTN_REDEEM_TROPHY = (AppiumBy.ID, "com.example.smileapp:id/btnRedeemTrophy")
    BTN_REDEEM_BADGE = (AppiumBy.ID, "com.example.smileapp:id/btnRedeemBadge")
    TV_REWARD_STATUS = (AppiumBy.ID, "com.example.smileapp:id/tvRewardStatus")

    def get_points_balance(self):
        return self.get_text(*self.TV_TOTAL_POINTS)

    def redeem_teddy_bear(self):
        self.click(*self.BTN_REDEEM_TEDDY)

    def redeem_trophy(self):
        self.click(*self.BTN_REDEEM_TROPHY)

    def redeem_badge(self):
        self.click(*self.BTN_REDEEM_BADGE)
