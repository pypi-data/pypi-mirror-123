Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const enzyme_1 = require("sentry-test/enzyme");
const projectSecurityAndPrivacy_1 = (0, tslib_1.__importDefault)(require("app/views/settings/projectSecurityAndPrivacy"));
// @ts-expect-error
const org = TestStubs.Organization();
// @ts-expect-error
const project = TestStubs.ProjectDetails();
// @ts-expect-error
const routerContext = TestStubs.routerContext([
    {
        // @ts-expect-error
        router: TestStubs.router({
            params: {
                projectId: project.slug,
                orgId: org.slug,
            },
        }),
    },
]);
function renderComponent(props) {
    var _a;
    const organization = (_a = props === null || props === void 0 ? void 0 : props.organization) !== null && _a !== void 0 ? _a : org;
    // @ts-expect-error
    MockApiClient.addMockResponse({
        url: `/projects/${organization.slug}/${project.slug}/`,
        method: 'GET',
        body: project,
    });
    return (0, enzyme_1.mountWithTheme)(<projectSecurityAndPrivacy_1.default project={project} {...routerContext} {...props} organization={organization}/>);
}
describe('projectSecurityAndPrivacy', function () {
    it('renders form fields', function () {
        const wrapper = renderComponent({});
        expect(wrapper.find('Switch[name="dataScrubber"]').prop('isActive')).toBeFalsy();
        expect(wrapper.find('Switch[name="dataScrubberDefaults"]').prop('isActive')).toBeFalsy();
        expect(wrapper.find('Switch[name="scrubIPAddresses"]').prop('isActive')).toBeFalsy();
        expect(wrapper.find('TextArea[name="sensitiveFields"]').prop('value')).toBe('creditcard\nssn');
        expect(wrapper.find('TextArea[name="safeFields"]').prop('value')).toBe('business-email\ncompany');
    });
    it('disables field when equivalent org setting is true', function () {
        const newOrganization = Object.assign({}, org);
        newOrganization.dataScrubber = true;
        newOrganization.scrubIPAddresses = false;
        const wrapper = renderComponent({ organization: newOrganization });
        expect(wrapper.find('Switch[name="scrubIPAddresses"]').prop('isDisabled')).toBe(false);
        expect(wrapper.find('Switch[name="scrubIPAddresses"]').prop('isActive')).toBeFalsy();
        expect(wrapper.find('Switch[name="dataScrubber"]').prop('isDisabled')).toBe(true);
        expect(wrapper.find('Switch[name="dataScrubber"]').prop('isActive')).toBe(true);
    });
});
//# sourceMappingURL=projectSecurityAndPrivacy.spec.jsx.map