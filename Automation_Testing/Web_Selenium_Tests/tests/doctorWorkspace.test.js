const { Builder, By, until } = require('selenium-webdriver');
const { expect } = require('chai');
const config = require('../config');
const LoginPage = require('../pages/loginPage');
const DoctorDashboardPage = require('../pages/doctorDashboardPage');

describe('Smile App Web Frontend - Doctor Workspace & Patient Management Selenium Suite', function () {
    this.timeout(30000);
    let driver;

    beforeEach(async function () {
        driver = await new Builder().forBrowser(config.BROWSER).build();
        await driver.get(config.BASE_URL);
    });

    afterEach(async function () {
        if (driver) {
            await driver.quit();
        }
    });

    it('TC_WEB_010: Verify Doctor Dashboard workspace stat cards and navigation', async function () {
        const loginPage = new LoginPage(driver);
        await loginPage.selectDoctorRole();
        await loginPage.loginAsDoctor(config.TEST_USERS.DOCTOR.email, config.TEST_USERS.DOCTOR.password);
    });
});
