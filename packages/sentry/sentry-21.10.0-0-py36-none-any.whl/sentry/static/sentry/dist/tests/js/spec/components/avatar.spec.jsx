Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const reactTestingLibrary_1 = require("sentry-test/reactTestingLibrary");
const avatar_1 = (0, tslib_1.__importDefault)(require("app/components/avatar"));
const gravatarBaseUrl = 'gravatarBaseUrl';
jest.mock('app/stores/configStore', () => ({
    getConfig: () => ({ gravatarBaseUrl }),
}));
describe('Avatar', function () {
    const avatar = {
        avatarType: 'gravatar',
        avatarUuid: '2d641b5d-8c74-44de-9cb6-fbd54701b35e',
    };
    const user = {
        id: '1',
        name: 'Jane Bloggs',
        username: 'janebloggs@example.com',
        email: 'janebloggs@example.com',
        ip_address: '127.0.0.1',
        avatar,
    };
    const userNameInitials = user.name
        .split(' ')
        .map(n => n[0])
        .join('');
    describe('render()', function () {
        it('has `avatar` className', function () {
            (0, reactTestingLibrary_1.mountWithTheme)(<avatar_1.default user={user}/>);
            const avatarElement = reactTestingLibrary_1.screen.getByTestId(`${avatar.avatarType}-avatar`);
            expect(avatarElement).toBeInTheDocument();
            expect(avatarElement).toHaveAttribute('title', user.name);
        });
        it('should show a gravatar when avatar type is gravatar', function () {
            return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
                (0, reactTestingLibrary_1.mountWithTheme)(<avatar_1.default user={user}/>);
                expect(reactTestingLibrary_1.screen.getByTestId(`${avatar.avatarType}-avatar`)).toBeInTheDocument();
                const avatarImage = yield reactTestingLibrary_1.screen.findByRole('img');
                expect(avatarImage).toHaveAttribute('src', `${gravatarBaseUrl}/avatar/a94c88e18c44e553497bf642449b6398?d=404&s=120`);
            });
        });
        it('should show an upload when avatar type is upload', function () {
            return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
                avatar.avatarType = 'upload';
                (0, reactTestingLibrary_1.mountWithTheme)(<avatar_1.default user={user}/>);
                expect(reactTestingLibrary_1.screen.getByTestId(`${avatar.avatarType}-avatar`)).toBeInTheDocument();
                const avatarImage = yield reactTestingLibrary_1.screen.findByRole('img');
                expect(avatarImage).toHaveAttribute('src', `/avatar/${avatar.avatarUuid}/?s=120`);
            });
        });
        it('should show an upload with the correct size (static 120 size)', function () {
            return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
                const avatar1 = (0, reactTestingLibrary_1.mountWithTheme)(<avatar_1.default user={user} size={76}/>);
                expect(yield reactTestingLibrary_1.screen.findByRole('img')).toHaveAttribute('src', `/avatar/${avatar.avatarUuid}/?s=120`);
                avatar1.unmount();
                const avatar2 = (0, reactTestingLibrary_1.mountWithTheme)(<avatar_1.default user={user} size={121}/>);
                expect(yield reactTestingLibrary_1.screen.findByRole('img')).toHaveAttribute('src', `/avatar/${avatar.avatarUuid}/?s=120`);
                avatar2.unmount();
                const avatar3 = (0, reactTestingLibrary_1.mountWithTheme)(<avatar_1.default user={user} size={32}/>);
                expect(yield reactTestingLibrary_1.screen.findByRole('img')).toHaveAttribute('src', `/avatar/${avatar.avatarUuid}/?s=120`);
                avatar3.unmount();
                (0, reactTestingLibrary_1.mountWithTheme)(<avatar_1.default user={user} size={1}/>);
                expect(yield reactTestingLibrary_1.screen.findByRole('img')).toHaveAttribute('src', `/avatar/${avatar.avatarUuid}/?s=120`);
            });
        });
        it('should not show upload or gravatar when avatar type is letter', function () {
            avatar.avatarType = 'letter_avatar';
            (0, reactTestingLibrary_1.mountWithTheme)(<avatar_1.default user={user}/>);
            expect(reactTestingLibrary_1.screen.getByTestId(`${avatar.avatarType}-avatar`)).toBeInTheDocument();
            expect(reactTestingLibrary_1.screen.getByText(userNameInitials)).toBeInTheDocument();
        });
        it('use letter avatar by default, when no avatar type is set and user has an email address', function () {
            (0, reactTestingLibrary_1.mountWithTheme)(<avatar_1.default user={Object.assign(Object.assign({}, user), { avatar: undefined })}/>);
            expect(reactTestingLibrary_1.screen.getByTestId(`${avatar.avatarType}-avatar`)).toBeInTheDocument();
            expect(reactTestingLibrary_1.screen.getByText(userNameInitials)).toBeInTheDocument();
        });
        it('should show a gravatar when no avatar type is set and user has an email address', function () {
            (0, reactTestingLibrary_1.mountWithTheme)(<avatar_1.default gravatar user={Object.assign(Object.assign({}, user), { avatar: undefined })}/>);
            const avatarElement = reactTestingLibrary_1.screen.getByTestId(`gravatar-avatar`);
            expect(avatarElement).toBeInTheDocument();
            expect(avatarElement).toHaveAttribute('title', user.name);
        });
        it('should not show a gravatar when no avatar type is set and user has no email address', function () {
            (0, reactTestingLibrary_1.mountWithTheme)(<avatar_1.default gravatar user={Object.assign(Object.assign({}, user), { email: '', avatar: undefined })}/>);
            expect(reactTestingLibrary_1.screen.getByTestId(`letter_avatar-avatar`)).toBeInTheDocument();
            expect(reactTestingLibrary_1.screen.getByText(userNameInitials)).toBeInTheDocument();
        });
        it('can display a team Avatar', function () {
            // @ts-expect-error
            const team = TestStubs.Team({ slug: 'test-team_test' });
            (0, reactTestingLibrary_1.mountWithTheme)(<avatar_1.default team={team}/>);
            expect(reactTestingLibrary_1.screen.getByTestId(`letter_avatar-avatar`)).toBeInTheDocument();
            expect(reactTestingLibrary_1.screen.getByText('TT')).toBeInTheDocument();
        });
        it('can display an organization Avatar', function () {
            // @ts-expect-error
            const organization = TestStubs.Organization({ slug: 'test-organization' });
            (0, reactTestingLibrary_1.mountWithTheme)(<avatar_1.default organization={organization}/>);
            expect(reactTestingLibrary_1.screen.getByTestId(`letter_avatar-avatar`)).toBeInTheDocument();
            expect(reactTestingLibrary_1.screen.getByText('TO')).toBeInTheDocument();
        });
        it('displays platform list icons for project Avatar', function () {
            // @ts-expect-error
            const project = TestStubs.Project({
                platforms: ['python', 'javascript'],
                platform: 'java',
            });
            (0, reactTestingLibrary_1.mountWithTheme)(<avatar_1.default project={project}/>);
            const platformIcon = reactTestingLibrary_1.screen.getByRole('img');
            expect(platformIcon).toBeInTheDocument();
            expect(platformIcon).toHaveAttribute('data-test-id', `platform-icon-${project.platform}`);
        });
        it('displays a fallback platform list for project Avatar using the `platform` specified during onboarding', function () {
            // @ts-expect-error
            const project = TestStubs.Project({ platform: 'java' });
            (0, reactTestingLibrary_1.mountWithTheme)(<avatar_1.default project={project}/>);
            const platformIcon = reactTestingLibrary_1.screen.getByRole('img');
            expect(platformIcon).toBeInTheDocument();
            expect(platformIcon).toHaveAttribute('data-test-id', `platform-icon-${project.platform}`);
        });
        it('uses onboarding project when platforms is an empty array', function () {
            // @ts-expect-error
            const project = TestStubs.Project({ platforms: [], platform: 'java' });
            (0, reactTestingLibrary_1.mountWithTheme)(<avatar_1.default project={project}/>);
            const platformIcon = reactTestingLibrary_1.screen.getByRole('img');
            expect(platformIcon).toBeInTheDocument();
            expect(platformIcon).toHaveAttribute('data-test-id', `platform-icon-${project.platform}`);
        });
    });
});
//# sourceMappingURL=avatar.spec.jsx.map