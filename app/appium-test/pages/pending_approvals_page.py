from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage

class PendingApprovalsPage(BasePage):
    """Page Object for PendingApprovalsActivity & PendingReviewsActivity."""

    RECYCLER_PENDING_USERS = (AppiumBy.ID, "com.example.smileapp:id/rvPendingApprovals")
    BTN_APPROVE_USER = (AppiumBy.ID, "com.example.smileapp:id/btnApproveUser")
    BTN_REJECT_USER = (AppiumBy.ID, "com.example.smileapp:id/btnRejectUser")
    RECYCLER_PENDING_VIDEOS = (AppiumBy.ID, "com.example.smileapp:id/rvPendingReviews")
    BTN_PLAY_VIDEO = (AppiumBy.ID, "com.example.smileapp:id/btnPlayVideo")
    BTN_AWARD_POINTS = (AppiumBy.ID, "com.example.smileapp:id/btnAwardPoints")

    def approve_first_user(self):
        self.click(*self.BTN_APPROVE_USER)

    def reject_first_user(self):
        self.click(*self.BTN_REJECT_USER)

    def play_review_video(self):
        self.click(*self.BTN_PLAY_VIDEO)

    def award_video_points(self):
        self.click(*self.BTN_AWARD_POINTS)
