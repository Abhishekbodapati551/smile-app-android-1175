const { By, until } = require('selenium-webdriver');
const config = require('../config');

class PatientDashboardPage {
    constructor(driver) {
        this.driver = driver;
        this.screenChildDashboard = By.id('screen-dashboard-child');
        this.welcomeMsg = By.id('child-welcome-msg');
        this.streakVal = By.id('child-streak');
        this.missionCard = By.xpath("//h3[contains(text(), \"Today's Mission\")]");
        this.pointsDisplay = By.id('points-display');
        this.rewardStoreBtn = By.xpath("//span[contains(text(), 'VIEW ALL')]");
        this.brushingModal = By.id('modal-brushing');
        this.btnStartBrush = By.id('btn-start-brush');
        this.timerVal = By.id('timer-val');
    }

    async isDashboardDisplayed() {
        const el = await this.driver.wait(until.elementLocated(this.screenChildDashboard), config.EXPLICIT_WAIT);
        return await el.isDisplayed();
    }

    async getWelcomeText() {
        const el = await this.driver.wait(until.elementLocated(this.welcomeMsg), config.EXPLICIT_WAIT);
        return await el.getText();
    }

    async openBrushingMission() {
        const card = await this.driver.findElement(this.missionCard);
        await card.click();
        await this.driver.wait(until.elementIsVisible(await this.driver.findElement(this.brushingModal)), config.EXPLICIT_WAIT);
    }

    async startBrushingTimer() {
        const btn = await this.driver.findElement(this.btnStartBrush);
        await btn.click();
    }
}

module.exports = PatientDashboardPage;
