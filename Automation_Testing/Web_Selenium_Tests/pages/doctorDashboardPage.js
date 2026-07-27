const { By, until } = require('selenium-webdriver');
const config = require('../config');

class DoctorDashboardPage {
    constructor(driver) {
        this.driver = driver;
        this.screenDoctorDashboard = By.id('screen-dashboard-doctor');
        this.welcomeMsg = By.id('doctor-welcome-msg');
        this.doctorIdDisplay = By.id('doctor-id-display');
        this.statPatients = By.id('stat-patients');
        this.statAppts = By.id('stat-appts');
        this.statApprovals = By.id('stat-approvals');
        this.statReviews = By.id('stat-reviews');
        this.btnSync = By.xpath("//button[contains(text(), 'SYNC DATA')]");
        this.btnScheduleVisit = By.xpath("//button[contains(text(), 'Schedule New Visit')]");
        this.modalAddAppt = By.id('modal-add-appt');
    }

    async isDashboardDisplayed() {
        const el = await this.driver.wait(until.elementLocated(this.screenDoctorDashboard), config.EXPLICIT_WAIT);
        return await el.isDisplayed();
    }

    async openScheduleVisitModal() {
        const btn = await this.driver.findElement(this.btnScheduleVisit);
        await btn.click();
        await this.driver.wait(until.elementIsVisible(await this.driver.findElement(this.modalAddAppt)), config.EXPLICIT_WAIT);
    }
}

module.exports = DoctorDashboardPage;
