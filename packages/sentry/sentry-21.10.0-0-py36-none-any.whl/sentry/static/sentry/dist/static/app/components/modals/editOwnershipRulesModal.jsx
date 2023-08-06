Object.defineProperty(exports, "__esModule", { value: true });
exports.modalCss = void 0;
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_2 = require("@emotion/react");
const locale_1 = require("app/locale");
const theme_1 = (0, tslib_1.__importDefault)(require("app/utils/theme"));
const editRulesModal_1 = (0, tslib_1.__importDefault)(require("app/views/settings/project/projectOwnership/editRulesModal"));
const EditOwnershipRulesModal = (_a) => {
    var { Body, Header, onSave } = _a, props = (0, tslib_1.__rest)(_a, ["Body", "Header", "onSave"]);
    return (<react_1.Fragment>
      <Header closeButton>{(0, locale_1.t)('Edit Ownership Rules')}</Header>
      <Body>
        <editRulesModal_1.default {...props} onSave={onSave}/>
      </Body>
    </react_1.Fragment>);
};
exports.modalCss = (0, react_2.css) `
  @media (min-width: ${theme_1.default.breakpoints[0]}) {
    width: 80%;
  }
  [role='document'] {
    overflow: initial;
  }
`;
exports.default = EditOwnershipRulesModal;
//# sourceMappingURL=editOwnershipRulesModal.jsx.map