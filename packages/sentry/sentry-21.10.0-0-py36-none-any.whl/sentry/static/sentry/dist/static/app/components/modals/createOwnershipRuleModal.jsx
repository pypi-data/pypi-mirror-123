Object.defineProperty(exports, "__esModule", { value: true });
exports.modalCss = void 0;
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_2 = require("@emotion/react");
const locale_1 = require("app/locale");
const theme_1 = (0, tslib_1.__importDefault)(require("app/utils/theme"));
const modal_1 = (0, tslib_1.__importDefault)(require("app/views/settings/project/projectOwnership/modal"));
const CreateOwnershipRuleModal = (_a) => {
    var { Body, Header, closeModal } = _a, props = (0, tslib_1.__rest)(_a, ["Body", "Header", "closeModal"]);
    const handleSuccess = () => {
        var _a;
        (_a = props.onClose) === null || _a === void 0 ? void 0 : _a.call(props);
        window.setTimeout(closeModal, 2000);
    };
    return (<react_1.Fragment>
      <Header closeButton>{(0, locale_1.t)('Create Ownership Rule')}</Header>
      <Body>
        <modal_1.default {...props} onSave={handleSuccess}/>
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
exports.default = CreateOwnershipRuleModal;
//# sourceMappingURL=createOwnershipRuleModal.jsx.map