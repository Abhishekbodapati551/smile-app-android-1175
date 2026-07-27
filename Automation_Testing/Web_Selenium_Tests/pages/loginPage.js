const { By, until } = require('selenium-webdriver');
const config = require('../config');

class LoginPage {
    constructor(driver) {
        this.driver = driver;
        
        # Start Screen Locators
        this.btnPatientRole = By.xpath("//button[contains(text(), \"I'M A PATIENT\")]");
        this.btnDoctorRole = By.xpath("//button[contains(text(), \"I'M A DOCTOR\")]");
        this.startScreen = By.id('screen-start');

        # Patient Login Locators
        this.screenLoginChild = By.id('screen-login-child');
        this.inputChildEmail = By.id('child-email');
        this.inputChildPassword = By.id('child-password');
        this.btnLoginChild = By.id('btn-login-child');

        # Doctor Login Locators
        this.screenLoginDoctor = By.id('screen-login-doctor');
        this.inputDoctorEmail = By.id('doctor-email');
        this.inputDoctorPassword = By.id('doctor-password');
        this.btnDoctorLogin = By.id('btn-login-doctor');

        # Register Locators
        this.screenRegister = By.id('screen-register');
        this.regRoleChildBtn = By.id('reg-role-child');
        this.regRoleDoctorBtn = By.id('reg-role-doctor');
        this.inputRegName = By.id('reg-name');
        this.inputRegEmail = By.id('reg-email');
        this.inputRegPassword = By.id('reg-password');
        this.inputRegDoctorId = By.id('reg-doctor-id');
        this.btnSignUp = By.id('btn-signup');
    }

    async openApp() {
        await this.driver.get(config.BASE_URL);
        await this.driver.wait(until.elementLocated(this.startScreen), config.EXPLICIT_WAIT);
    }

    async selectPatientRole() {
        const btn = await this.driver.wait(until.elementLocated(this.btnPatientRole), config.EXPLICIT_WAIT);
        await btn.click();
        await this.driver.wait(until.elementIsVisible(await this.driver.findElement(this.screenLoginChild)), config.EXPLICIT_WAIT);
    }

    async selectDoctorRole() {
        const btn = await this.driver.wait(until.elementLocated(this.btnDoctorRole), config.EXPLICIT_WAIT);
        await btn.click();
        await this.driver.wait(until.elementIsVisible(await this.driver.findElement(this.screenLoginDoctor)), config.EXPLICIT_WAIT);
    }

    async loginAsPatient(email, password) {
        await this.driver.findElement(this.inputChildEmail).clear();
        await this.driver.findElement(this.inputChildEmail).sendKeys(email);
        await this.driver.findElement(this.inputChildPassword).clear();
        await this.driver.findElement(this.inputChildPassword).sendKeys(password);
        await this.driver.findElement(this.btnLoginChild).click();
    }

    async loginAsDoctor(email, password) {
        await this.driver.findElement(this.inputDoctorEmail).clear();
        await this.driver.findElement(this.inputDoctorEmail).sendKeys(email);
        await this.driver.findElement(this.inputDoctorPassword).clear();
        await this.driver.findElement(this.inputDoctorPassword).sendKeys(password);
        await this.driver.findElement(this.btnDoctorLogin).click();
    }

    async fillRegistrationForm(name, email, password, role = 'child', doctorId = '1176') {
        if (role === 'doctor') {
            await this.driver.findElement(this.regRoleDoctorBtn).click();
        } else {
            await this.driver.findElement(this.regRoleChildBtn).click();
        }
        await this.driver.findElement(this.inputRegName).sendKeys(name);
        await this.driver.findElement(this.inputRegEmail).sendKeys(email);
        await this.driver.findElement(this.inputRegPassword).sendKeys(password);
        if (role === 'child') {
            await this.driver.findElement(this.inputRegDoctorId).sendKeys(doctorId);
        }
        await this.driver.findElement(this.btnSignUp).click();
    }
}

module.exports = LoginPage;
