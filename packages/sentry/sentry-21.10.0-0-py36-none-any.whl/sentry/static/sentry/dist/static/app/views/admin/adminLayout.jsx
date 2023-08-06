Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_document_title_1 = (0, tslib_1.__importDefault)(require("react-document-title"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const settingsLayout_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsLayout"));
const settingsNavigation_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsNavigation"));
const AdminNavigation = () => (<settingsNavigation_1.default stickyTop="0" navigationObjects={[
        {
            name: 'System Status',
            items: [
                { path: '/manage/', index: true, title: 'Overview' },
                { path: '/manage/buffer/', title: 'Buffer' },
                { path: '/manage/queue/', title: 'Queue' },
                { path: '/manage/quotas/', title: 'Quotas' },
                { path: '/manage/status/environment/', title: 'Environment' },
                { path: '/manage/status/packages/', title: 'Packages' },
                { path: '/manage/status/mail/', title: 'Mail' },
                { path: '/manage/status/warnings/', title: 'Warnings' },
                { path: '/manage/settings/', title: 'Settings' },
            ],
        },
        {
            name: 'Manage',
            items: [
                { path: '/manage/organizations/', title: 'Organizations' },
                { path: '/manage/projects/', title: 'Projects' },
                { path: '/manage/users/', title: 'Users' },
            ],
        },
    ]}/>);
function AdminLayout(_a) {
    var { children } = _a, props = (0, tslib_1.__rest)(_a, ["children"]);
    return (<react_document_title_1.default title="Sentry Admin">
      <Page>
        <settingsLayout_1.default renderNavigation={AdminNavigation} {...props}>
          {children}
        </settingsLayout_1.default>
      </Page>
    </react_document_title_1.default>);
}
exports.default = AdminLayout;
const Page = (0, styled_1.default)('div') `
  display: flex;
  flex-grow: 1;
  margin-bottom: -20px;
`;
//# sourceMappingURL=adminLayout.jsx.map