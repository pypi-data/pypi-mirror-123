Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_document_title_1 = (0, tslib_1.__importDefault)(require("react-document-title"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const createProject_1 = (0, tslib_1.__importDefault)(require("app/views/projectInstall/createProject"));
const NewProject = () => (<Container>
    <div className="container">
      <Content>
        <react_document_title_1.default title="Sentry"/>
        <createProject_1.default />
      </Content>
    </div>
  </Container>);
const Container = (0, styled_1.default)('div') `
  flex: 1;
  background: ${p => p.theme.background};
  margin-bottom: -${(0, space_1.default)(3)}; /* cleans up a bg gap at bottom */
`;
const Content = (0, styled_1.default)('div') `
  margin-top: ${(0, space_1.default)(3)};
`;
exports.default = NewProject;
//# sourceMappingURL=newProject.jsx.map