Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const icons_1 = require("app/icons");
const animations_1 = require("app/styles/animations");
const spinner_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/spinner"));
/**
 * ControlState (i.e. loading/error icons) for form fields
 */
const ControlState = ({ isSaving, isSaved, error }) => (<react_1.Fragment>
    {isSaving ? (<ControlStateWrapper>
        <FormSpinner />
      </ControlStateWrapper>) : isSaved ? (<ControlStateWrapper>
        <FieldIsSaved>
          <icons_1.IconCheckmark size="18px"/>
        </FieldIsSaved>
      </ControlStateWrapper>) : null}

    {error ? (<ControlStateWrapper>
        <FieldError>
          <icons_1.IconWarning size="18px"/>
        </FieldError>
      </ControlStateWrapper>) : null}
  </react_1.Fragment>);
const ControlStateWrapper = (0, styled_1.default)('div') `
  line-height: 0;
  padding: 0 8px;
`;
const FieldIsSaved = (0, styled_1.default)('div') `
  color: ${p => p.theme.green300};
  animation: ${animations_1.fadeOut} 0.3s ease 2s 1 forwards;
  position: absolute;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  display: flex;
  align-items: center;
  justify-content: center;
`;
const FormSpinner = (0, styled_1.default)(spinner_1.default) `
  margin-left: 0;
`;
const FieldError = (0, styled_1.default)('div') `
  color: ${p => p.theme.red300};
  animation: ${() => (0, animations_1.pulse)(1.15)} 1s ease infinite;
`;
exports.default = ControlState;
//# sourceMappingURL=controlState.jsx.map