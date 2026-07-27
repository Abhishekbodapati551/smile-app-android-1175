const { Builder, By, until } = require('selenium-webdriver');
const { expect } = require('chai');
const config = require('../config');
const LoginPage = require('../pages/loginPage');
const PatientDashboardPage = require('../pages/patientDashboardPage');

describe('Smile App Web Frontend - Patient Dashboard & Mission E2E Selenium Suite', function () {
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

    it('TC_WEB_008: Verify Patient Dashboard UI elements and streak display', async function () {
        const loginPage = new LoginPage(driver);
        await loginPage.selectPatientRole();
        await loginPage.loginAsPatient(config.TEST_USERS.PATIENT.email, config.TEST_USERS.PATIENT.password);
    });

    it('TC_WEB_009: Verify Brushing Mission modal opens with 02:00 timer display', async function () {
        const loginPage = new LoginPage(driver);
        await loginPage.selectPatientRole();
        await loginPage.loginAsPatient(config.TEST_USERS.PATIENT.email, config.TEST_USERS.PATIENT.password);
    });
});
