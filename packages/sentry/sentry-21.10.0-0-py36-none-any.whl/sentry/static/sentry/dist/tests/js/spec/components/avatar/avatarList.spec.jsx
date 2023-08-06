Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const reactTestingLibrary_1 = require("sentry-test/reactTestingLibrary");
const avatarList_1 = (0, tslib_1.__importDefault)(require("app/components/avatar/avatarList"));
function renderComponent(avatarUsersSixUsers) {
    return (0, reactTestingLibrary_1.mountWithTheme)(<avatarList_1.default users={avatarUsersSixUsers}/>);
}
describe('AvatarList', () => {
    // @ts-expect-error
    const user = TestStubs.User();
    it('renders with user letter avatars', () => {
        const users = [
            Object.assign(Object.assign({}, user), { id: '1', name: 'AB' }),
            Object.assign(Object.assign({}, user), { id: '2', name: 'BC' }),
        ];
        const { container } = renderComponent(users);
        expect(reactTestingLibrary_1.screen.getByText('A')).toBeTruthy();
        expect(reactTestingLibrary_1.screen.getByText('B')).toBeTruthy();
        expect(reactTestingLibrary_1.screen.queryByTestId('avatarList-collapsedusers')).toBeNull();
        expect(container).toSnapshot();
    });
    it('renders with collapsed avatar count if > 5 users', () => {
        const users = [
            Object.assign(Object.assign({}, user), { id: '1', name: 'AB' }),
            Object.assign(Object.assign({}, user), { id: '2', name: 'BC' }),
            Object.assign(Object.assign({}, user), { id: '3', name: 'CD' }),
            Object.assign(Object.assign({}, user), { id: '4', name: 'DE' }),
            Object.assign(Object.assign({}, user), { id: '5', name: 'EF' }),
            Object.assign(Object.assign({}, user), { id: '6', name: 'FG' }),
        ];
        const { container } = renderComponent(users);
        expect(reactTestingLibrary_1.screen.queryAllByText(users[0].name.charAt(0))).toBeTruthy();
        expect(reactTestingLibrary_1.screen.queryAllByText(users[1].name.charAt(0))).toBeTruthy();
        expect(reactTestingLibrary_1.screen.queryAllByText(users[2].name.charAt(0))).toBeTruthy();
        expect(reactTestingLibrary_1.screen.queryAllByText(users[3].name.charAt(0))).toBeTruthy();
        expect(reactTestingLibrary_1.screen.queryAllByText(users[4].name.charAt(0))).toBeTruthy();
        expect(reactTestingLibrary_1.screen.queryByText(users[5].name.charAt(0))).toBeNull();
        expect(reactTestingLibrary_1.screen.getByTestId('avatarList-collapsedusers')).toBeTruthy();
        expect(container).toSnapshot();
    });
});
//# sourceMappingURL=avatarList.spec.jsx.map