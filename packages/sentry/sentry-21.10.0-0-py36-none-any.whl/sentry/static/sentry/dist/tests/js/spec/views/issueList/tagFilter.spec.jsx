Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const reactTestingLibrary_1 = require("sentry-test/reactTestingLibrary");
const tagFilter_1 = (0, tslib_1.__importDefault)(require("app/views/issueList/tagFilter"));
describe('IssueListTagFilter', function () {
    // @ts-expect-error
    MockApiClient.clearMockResponses();
    const selectMock = jest.fn();
    const tag = { key: 'browser', name: 'Browser' };
    const tagValueLoader = () => new Promise(resolve => resolve([
        {
            count: 0,
            firstSeen: '2018-05-30T11:33:46.535Z',
            key: 'foo',
            lastSeen: '2018-05-30T11:33:46.535Z',
            name: 'foo',
            value: 'foo',
            id: 'foo',
            ip_address: '192.168.1.1',
            email: 'foo@boy.cat',
            username: 'foo',
        },
        {
            count: 0,
            firstSeen: '2018-05-30T11:33:46.535Z',
            key: 'fooBaar',
            lastSeen: '2018-05-30T11:33:46.535Z',
            name: 'fooBaar',
            value: 'fooBaar',
            id: 'fooBaar',
            ip_address: '192.168.1.1',
            email: 'fooBaar@boy.cat',
            username: 'ffooBaaroo',
        },
    ]));
    it('calls API and renders options when opened', function () {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            (0, reactTestingLibrary_1.mountWithTheme)(<tagFilter_1.default tag={tag} value="" onSelect={selectMock} tagValueLoader={tagValueLoader}/>);
            // changes dropdown input value
            const input = reactTestingLibrary_1.screen.getByLabelText(tag.key);
            reactTestingLibrary_1.fireEvent.change(input, { target: { value: 'foo' } });
            // waits for the loading indicator to disappear
            const loadingIndicator = reactTestingLibrary_1.screen.getByText('Loading\u2026');
            yield (0, reactTestingLibrary_1.waitFor)(() => expect(loadingIndicator).not.toBeInTheDocument());
            // the result has a length of 2, because when performing a search,
            // an element containing the same value is present in the rendered HTML markup
            const allFoo = reactTestingLibrary_1.screen.getAllByText('foo');
            // selects menu option
            const menuOptionFoo = allFoo[1];
            reactTestingLibrary_1.fireEvent.click(menuOptionFoo);
            expect(selectMock).toHaveBeenCalledWith(tag, 'foo');
        });
    });
});
//# sourceMappingURL=tagFilter.spec.jsx.map