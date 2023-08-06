Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const enzyme_1 = require("sentry-test/enzyme");
const accountDetails_1 = (0, tslib_1.__importDefault)(require("app/data/forms/accountDetails"));
const projectGeneralSettings_1 = require("app/data/forms/projectGeneralSettings");
const jsonForm_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/jsonForm"));
// @ts-expect-error
const user = TestStubs.User({});
describe('JsonForm', function () {
    describe('form prop', function () {
        it('default', function () {
            const wrapper = (0, enzyme_1.mountWithTheme)(<jsonForm_1.default forms={accountDetails_1.default} additionalFieldProps={{ user }}/>);
            expect(wrapper).toSnapshot();
        });
        it('missing additionalFieldProps required in "valid" prop', function () {
            // eslint-disable-next-line no-console
            console.error = jest.fn();
            try {
                (0, enzyme_1.mountWithTheme)(<jsonForm_1.default forms={accountDetails_1.default}/>);
            }
            catch (error) {
                expect(error.message).toBe("Cannot read property 'email' of undefined");
            }
        });
        it('should ALWAYS hide panel, if all fields have visible set to false  AND there is no renderHeader & renderFooter -  visible prop is of type boolean', function () {
            const modifiedAccountDetails = accountDetails_1.default.map(accountDetailsField => (Object.assign(Object.assign({}, accountDetailsField), { fields: accountDetailsField.fields.map(field => (Object.assign(Object.assign({}, field), { visible: false }))) })));
            const wrapper = (0, enzyme_1.mountWithTheme)(<jsonForm_1.default forms={modifiedAccountDetails} additionalFieldProps={{ user }}/>);
            expect(wrapper.find('FormPanel')).toHaveLength(0);
        });
        it('should ALWAYS hide panel, if all fields have visible set to false AND there is no renderHeader & renderFooter -  visible prop is of type func', function () {
            const modifiedAccountDetails = accountDetails_1.default.map(accountDetailsField => (Object.assign(Object.assign({}, accountDetailsField), { fields: accountDetailsField.fields.map(field => (Object.assign(Object.assign({}, field), { visible: () => false }))) })));
            const wrapper = (0, enzyme_1.mountWithTheme)(<jsonForm_1.default forms={modifiedAccountDetails} additionalFieldProps={{ user }}/>);
            expect(wrapper.find('FormPanel')).toHaveLength(0);
        });
        it('should NOT hide panel, if at least one field has visible set to true -  no visible prop (1 field) + visible prop is of type func (2 field)', function () {
            // accountDetailsFields has two fields. The second field will always have visible set to false, because the username and the email are the same 'foo@example.com'
            const wrapper = (0, enzyme_1.mountWithTheme)(<jsonForm_1.default forms={accountDetails_1.default} additionalFieldProps={{ user }}/>);
            expect(wrapper.find('FormPanel')).toHaveLength(1);
            expect(wrapper.find('input')).toHaveLength(1);
        });
        it('should NOT hide panel, if all fields have visible set to false AND a prop renderHeader is passed', function () {
            const modifiedAccountDetails = accountDetails_1.default.map(accountDetailsField => (Object.assign(Object.assign({}, accountDetailsField), { fields: accountDetailsField.fields.map(field => (Object.assign(Object.assign({}, field), { visible: false }))) })));
            const wrapper = (0, enzyme_1.mountWithTheme)(<jsonForm_1.default forms={modifiedAccountDetails} additionalFieldProps={{ user }} renderHeader={() => <div>this is a Header </div>}/>);
            expect(wrapper.find('FormPanel')).toHaveLength(1);
            expect(wrapper.find('input')).toHaveLength(0);
        });
        it('should NOT hide panel, if all fields have visible set to false AND a prop renderFooter is passed', function () {
            const modifiedAccountDetails = accountDetails_1.default.map(accountDetailsField => (Object.assign(Object.assign({}, accountDetailsField), { fields: accountDetailsField.fields.map(field => (Object.assign(Object.assign({}, field), { visible: false }))) })));
            const wrapper = (0, enzyme_1.mountWithTheme)(<jsonForm_1.default forms={modifiedAccountDetails} additionalFieldProps={{ user }} renderFooter={() => <div>this is a Footer </div>}/>);
            expect(wrapper.find('FormPanel')).toHaveLength(1);
            expect(wrapper.find('input')).toHaveLength(0);
        });
    });
    describe('fields prop', function () {
        const jsonFormFields = [projectGeneralSettings_1.fields.slug, projectGeneralSettings_1.fields.platform];
        it('default', function () {
            const wrapper = (0, enzyme_1.mountWithTheme)(<jsonForm_1.default fields={jsonFormFields}/>);
            expect(wrapper).toSnapshot();
        });
        it('missing additionalFieldProps required in "valid" prop', function () {
            // eslint-disable-next-line no-console
            console.error = jest.fn();
            try {
                (0, enzyme_1.mountWithTheme)(<jsonForm_1.default fields={[Object.assign(Object.assign({}, jsonFormFields[0]), { visible: ({ test }) => !!test.email })]}/>);
            }
            catch (error) {
                expect(error.message).toBe("Cannot read property 'email' of undefined");
            }
        });
        it('should NOT hide panel, if at least one field has visible set to true - no visible prop', function () {
            // slug and platform have no visible prop, that means they will be always visible
            const wrapper = (0, enzyme_1.mountWithTheme)(<jsonForm_1.default fields={jsonFormFields}/>);
            expect(wrapper.find('FormPanel')).toHaveLength(1);
            expect(wrapper.find('input[type="text"]')).toHaveLength(2);
        });
        it('should NOT hide panel, if at least one field has visible set to true -  visible prop is of type boolean', function () {
            // slug and platform have no visible prop, that means they will be always visible
            const wrapper = (0, enzyme_1.mountWithTheme)(<jsonForm_1.default fields={jsonFormFields.map(field => (Object.assign(Object.assign({}, field), { visible: true })))}/>);
            expect(wrapper.find('FormPanel')).toHaveLength(1);
            expect(wrapper.find('input[type="text"]')).toHaveLength(2);
        });
        it('should NOT hide panel, if at least one field has visible set to true -  visible prop is of type func', function () {
            // slug and platform have no visible prop, that means they will be always visible
            const wrapper = (0, enzyme_1.mountWithTheme)(<jsonForm_1.default fields={jsonFormFields.map(field => (Object.assign(Object.assign({}, field), { visible: () => true })))}/>);
            expect(wrapper.find('FormPanel')).toHaveLength(1);
            expect(wrapper.find('input[type="text"]')).toHaveLength(2);
        });
        it('should ALWAYS hide panel, if all fields have visible set to false -  visible prop is of type boolean', function () {
            // slug and platform have no visible prop, that means they will be always visible
            const wrapper = (0, enzyme_1.mountWithTheme)(<jsonForm_1.default fields={jsonFormFields.map(field => (Object.assign(Object.assign({}, field), { visible: false })))}/>);
            expect(wrapper.find('FormPanel')).toHaveLength(0);
        });
        it('should ALWAYS hide panel, if all fields have visible set to false - visible prop is of type function', function () {
            // slug and platform have no visible prop, that means they will be always visible
            const wrapper = (0, enzyme_1.mountWithTheme)(<jsonForm_1.default fields={jsonFormFields.map(field => (Object.assign(Object.assign({}, field), { visible: () => false })))}/>);
            expect(wrapper.find('FormPanel')).toHaveLength(0);
        });
    });
});
//# sourceMappingURL=jsonForm.spec.jsx.map