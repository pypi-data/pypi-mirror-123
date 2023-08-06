Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const controlState_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/field/controlState"));
const types_1 = require("../../types");
const EventIdFieldStatusIcon = ({ status, onClickIconClose }) => {
    switch (status) {
        case types_1.EventIdStatus.ERROR:
        case types_1.EventIdStatus.INVALID:
        case types_1.EventIdStatus.NOT_FOUND:
            return (<CloseIcon onClick={onClickIconClose}>
          <tooltip_1.default title={(0, locale_1.t)('Clear event ID')}>
            <StyledIconClose size="xs"/>
          </tooltip_1.default>
        </CloseIcon>);
        case types_1.EventIdStatus.LOADING:
            return <controlState_1.default isSaving/>;
        case types_1.EventIdStatus.LOADED:
            return <icons_1.IconCheckmark color="green300"/>;
        default:
            return null;
    }
};
exports.default = EventIdFieldStatusIcon;
const CloseIcon = (0, styled_1.default)('div') `
  :first-child {
    line-height: 0;
  }
`;
const StyledIconClose = (0, styled_1.default)(icons_1.IconClose) `
  color: ${p => p.theme.gray200};
  :hover {
    color: ${p => p.theme.gray300};
  }
  cursor: pointer;
`;
//# sourceMappingURL=eventIdFieldStatusIcon.jsx.map