Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const initializeOrg_1 = require("sentry-test/initializeOrg");
const reactTestingLibrary_1 = require("sentry-test/reactTestingLibrary");
const eventAttachments_1 = (0, tslib_1.__importDefault)(require("app/components/events/eventAttachments"));
describe('EventAttachments', function () {
    const { routerContext, organization, project } = (0, initializeOrg_1.initializeOrg)();
    // @ts-expect-error
    const event = TestStubs.Event({ metadata: { stripped_crash: true } });
    const props = {
        orgId: organization.slug,
        projectId: project.slug,
        location: routerContext.context.location,
        attachments: [],
        onDeleteAttachment: jest.fn(),
        event,
    };
    it('shows attachments limit reached notice', function () {
        (0, reactTestingLibrary_1.mountWithTheme)(<eventAttachments_1.default {...props}/>);
        expect(reactTestingLibrary_1.screen.getByText('Attachments (0)')).toBeInTheDocument();
        expect(reactTestingLibrary_1.screen.getByRole('link', { name: 'View crashes' })).toHaveAttribute('href', '');
        expect(reactTestingLibrary_1.screen.getByRole('link', { name: 'configure limit' })).toHaveAttribute('href', `/settings/${props.orgId}/projects/${props.projectId}/security-and-privacy/`);
        expect(reactTestingLibrary_1.screen.getByText('Your limit of stored crash reports has been reached for this issue.')).toBeInTheDocument();
    });
    it('does not render anything if no attachments (nor stripped) are available', function () {
        const { container } = (0, reactTestingLibrary_1.mountWithTheme)(<eventAttachments_1.default {...props} event={Object.assign(Object.assign({}, event), { metadata: { stripped_crash: false } })}/>);
        expect(container).toBeEmptyDOMElement();
    });
});
//# sourceMappingURL=eventAttachments.spec.jsx.map