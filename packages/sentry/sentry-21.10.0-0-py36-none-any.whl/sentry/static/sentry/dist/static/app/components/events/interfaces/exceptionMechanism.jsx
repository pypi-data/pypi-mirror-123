Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_2 = require("@emotion/react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const forOwn_1 = (0, tslib_1.__importDefault)(require("lodash/forOwn"));
const isNil_1 = (0, tslib_1.__importDefault)(require("lodash/isNil"));
const isObject_1 = (0, tslib_1.__importDefault)(require("lodash/isObject"));
const hovercard_1 = (0, tslib_1.__importDefault)(require("app/components/hovercard"));
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const pill_1 = (0, tslib_1.__importDefault)(require("app/components/pill"));
const pills_1 = (0, tslib_1.__importDefault)(require("app/components/pills"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const utils_1 = require("app/utils");
class ExceptionMechanism extends react_1.Component {
    render() {
        const mechanism = this.props.data;
        const { type, description, help_link, handled, meta = {}, data = {} } = mechanism;
        const { errno, signal, mach_exception } = meta;
        const linkElement = help_link && (0, utils_1.isUrl)(help_link) && (<StyledExternalLink href={help_link}>
        <icons_1.IconOpen size="xs"/>
      </StyledExternalLink>);
        const descriptionElement = description && (<hovercard_1.default header={<span>
            <Details>{(0, locale_1.t)('Details')}</Details> {linkElement}
          </span>} body={description}>
        <StyledIconInfo size="14px"/>
      </hovercard_1.default>);
        const pills = [
            <pill_1.default key="mechanism" name="mechanism" value={type || 'unknown'}>
        {descriptionElement || linkElement}
      </pill_1.default>,
        ];
        if (!(0, isNil_1.default)(handled)) {
            pills.push(<pill_1.default key="handled" name="handled" value={handled}/>);
        }
        if (errno) {
            const value = errno.name || errno.number;
            pills.push(<pill_1.default key="errno" name="errno" value={value}/>);
        }
        if (mach_exception) {
            const value = mach_exception.name || mach_exception.exception;
            pills.push(<pill_1.default key="mach" name="mach exception" value={value}/>);
        }
        if (signal) {
            const code = signal.code_name || `${(0, locale_1.t)('code')} ${signal.code}`;
            const name = signal.name || signal.number;
            const value = (0, isNil_1.default)(signal.code) ? name : `${name} (${code})`;
            pills.push(<pill_1.default key="signal" name="signal" value={value}/>);
        }
        (0, forOwn_1.default)(data, (value, key) => {
            if (!(0, isObject_1.default)(value)) {
                pills.push(<pill_1.default key={`data:${key}`} name={key} value={value}/>);
            }
        });
        return (<Wrapper>
        <StyledPills>{pills}</StyledPills>
      </Wrapper>);
    }
}
exports.default = ExceptionMechanism;
const Wrapper = (0, styled_1.default)('div') `
  margin: ${(0, space_1.default)(2)} 0;
`;
const iconStyle = (p) => (0, react_2.css) `
  transition: 0.1s linear color;
  color: ${p.theme.gray300};
  :hover {
    color: ${p.theme.gray500};
  }
`;
const StyledExternalLink = (0, styled_1.default)(externalLink_1.default) `
  display: inline-flex !important;
  ${iconStyle};
`;
const Details = (0, styled_1.default)('span') `
  margin-right: ${(0, space_1.default)(1)};
`;
const StyledPills = (0, styled_1.default)(pills_1.default) `
  span:nth-of-type(2) {
    display: inline;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
`;
const StyledIconInfo = (0, styled_1.default)(icons_1.IconInfo) `
  display: flex;
  ${iconStyle};
`;
//# sourceMappingURL=exceptionMechanism.jsx.map