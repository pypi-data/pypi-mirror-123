Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const enzyme_1 = require("sentry-test/enzyme");
const modal_1 = require("app/actionCreators/modal");
const debugImageDetails_1 = (0, tslib_1.__importStar)(require("app/components/events/interfaces/debugMeta-v2/debugImageDetails"));
const utils_1 = require("app/components/events/interfaces/debugMeta-v2/utils");
const globalModal_1 = (0, tslib_1.__importDefault)(require("app/components/globalModal"));
describe('Debug Meta - Image Details Candidates', function () {
    let wrapper;
    const projSlug = 'foo';
    // @ts-expect-error
    const organization = TestStubs.Organization();
    // @ts-expect-error
    const event = TestStubs.Event();
    // @ts-expect-error
    const eventEntryDebugMeta = TestStubs.EventEntryDebugMeta();
    const { data } = eventEntryDebugMeta;
    const { images } = data;
    const debugImage = images[0];
    beforeAll(function () {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            // @ts-expect-error
            MockApiClient.addMockResponse({
                url: `/projects/${organization.slug}/${projSlug}/files/dsyms/?debug_id=${debugImage.debug_id}`,
                method: 'GET',
                body: [],
            });
            // @ts-expect-error
            MockApiClient.addMockResponse({
                url: `/builtin-symbol-sources/`,
                method: 'GET',
                body: [],
            });
            wrapper = (0, enzyme_1.mountWithTheme)(<globalModal_1.default />);
            (0, modal_1.openModal)(modalProps => (<debugImageDetails_1.default {...modalProps} image={debugImage} organization={organization} projSlug={projSlug} event={event}/>), {
                modalCss: debugImageDetails_1.modalCss,
                onClose: jest.fn(),
            });
            // @ts-expect-error
            yield tick();
            wrapper.update();
        });
    });
    it('Image Details Modal is open', () => {
        const fileName = wrapper.find('Title FileName');
        expect(fileName.text()).toEqual((0, utils_1.getFileName)(debugImage.code_file));
    });
    it('Image Candidates correctly sorted', () => {
        const candidates = wrapper.find('Candidate');
        // Check status order.
        // The UI shall sort the candidates by status. However, this sorting is not alphabetical but in the following order:
        // Permissions -> Failed -> Ok -> Deleted (previous Ok) -> Unapplied -> Not Found
        const statusColumns = candidates
            .find('Status')
            .map(statusColumn => statusColumn.text());
        expect(statusColumns).toEqual(['Failed', 'Failed', 'Failed', 'Deleted']);
        const informationColumn = candidates.find('InformationColumn');
        // Check source names order.
        // The UI shall sort the candidates by source name (alphabetical)
        const sourceNames = informationColumn
            .find('[data-test-id="source_name"]')
            .map(sourceName => sourceName.text());
        expect(sourceNames).toEqual(['America', 'Austria', 'Belgium', 'Sentry']);
        // Check location order.
        // The UI shall sort the candidates by source location (alphabetical)
        const locations = informationColumn
            .find('FilenameOrLocation')
            .map(location => location.text());
        // Only 3 results are returned, as the UI only displays the Location component
        // when the location is defined and when it is not internal
        expect(locations).toEqual(['arizona', 'burgenland', 'brussels']);
    });
});
//# sourceMappingURL=imageDetailsCandidates.spec.jsx.map