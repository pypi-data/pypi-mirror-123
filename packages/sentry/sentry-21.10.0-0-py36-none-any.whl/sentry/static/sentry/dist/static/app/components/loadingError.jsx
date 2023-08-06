Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const panels_1 = require("app/components/panels");
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
/**
 * Renders an Alert box of type "error". Renders a "Retry" button only if a `onRetry` callback is defined.
 */
class LoadingError extends React.Component {
    shouldComponentUpdate() {
        return false;
    }
    render() {
        const { message, onRetry } = this.props;
        return (<StyledAlert type="error">
        <Content>
          <icons_1.IconInfo size="lg"/>
          <div data-test-id="loading-error-message">{message}</div>
          {onRetry && (<button_1.default onClick={onRetry} type="button" priority="default" size="small">
              {(0, locale_1.t)('Retry')}
            </button_1.default>)}
        </Content>
      </StyledAlert>);
    }
}
LoadingError.defaultProps = {
    message: (0, locale_1.t)('There was an error loading data.'),
};
exports.default = LoadingError;
const StyledAlert = (0, styled_1.default)(alert_1.default) `
  ${ /* sc-selector */panels_1.Panel} & {
    border-radius: 0;
    border-width: 1px 0;
  }
`;
const Content = (0, styled_1.default)('div') `
  display: grid;
  grid-gap: ${(0, space_1.default)(1)};
  grid-template-columns: min-content auto max-content;
  align-items: center;
`;
//# sourceMappingURL=loadingError.jsx.map