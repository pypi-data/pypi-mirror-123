Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const capitalize_1 = (0, tslib_1.__importDefault)(require("lodash/capitalize"));
const list_1 = (0, tslib_1.__importDefault)(require("app/components/list"));
const listItem_1 = (0, tslib_1.__importDefault)(require("app/components/list/listItem"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const chunks_1 = (0, tslib_1.__importDefault)(require("./chunks"));
const utils_1 = require("./utils");
const valueElement_1 = (0, tslib_1.__importDefault)(require("./valueElement"));
const AnnotatedText = (_a) => {
    var { value, meta, className } = _a, props = (0, tslib_1.__rest)(_a, ["value", "meta", "className"]);
    const renderValue = () => {
        var _a, _b;
        if (((_a = meta === null || meta === void 0 ? void 0 : meta.chunks) === null || _a === void 0 ? void 0 : _a.length) && meta.chunks.length > 1) {
            return <chunks_1.default chunks={meta.chunks}/>;
        }
        const element = <valueElement_1.default value={value} meta={meta}/>;
        if ((_b = meta === null || meta === void 0 ? void 0 : meta.rem) === null || _b === void 0 ? void 0 : _b.length) {
            const title = (0, utils_1.getTooltipText)({ rule_id: meta.rem[0][0], remark: meta.rem[0][1] });
            return <tooltip_1.default title={title}>{element}</tooltip_1.default>;
        }
        return element;
    };
    const formatErrorKind = (kind) => {
        return (0, capitalize_1.default)(kind.replace(/_/g, ' '));
    };
    const getErrorMessage = (error) => {
        var _a;
        const errorMessage = [];
        if (Array.isArray(error)) {
            if (error[0]) {
                errorMessage.push(formatErrorKind(error[0]));
            }
            if ((_a = error[1]) === null || _a === void 0 ? void 0 : _a.reason) {
                errorMessage.push(`(${error[1].reason})`);
            }
        }
        else {
            errorMessage.push(formatErrorKind(error));
        }
        return errorMessage.join(' ');
    };
    const getTooltipTitle = (errors) => {
        if (errors.length === 1) {
            return <TooltipTitle>{(0, locale_1.t)('Error: %s', getErrorMessage(errors[0]))}</TooltipTitle>;
        }
        return (<TooltipTitle>
        <span>{(0, locale_1.t)('Errors:')}</span>
        <StyledList symbol="bullet">
          {errors.map((error, index) => (<listItem_1.default key={index}>{getErrorMessage(error)}</listItem_1.default>))}
        </StyledList>
      </TooltipTitle>);
    };
    const renderErrors = (errors) => {
        if (!errors.length) {
            return null;
        }
        return (<StyledTooltipError title={getTooltipTitle(errors)}>
        <StyledIconWarning color="red300"/>
      </StyledTooltipError>);
    };
    return (<span className={className} {...props}>
      {renderValue()}
      {(meta === null || meta === void 0 ? void 0 : meta.err) && renderErrors(meta.err)}
    </span>);
};
exports.default = AnnotatedText;
const StyledTooltipError = (0, styled_1.default)(tooltip_1.default) `
  margin-left: ${(0, space_1.default)(0.75)};
  vertical-align: middle;
`;
const StyledList = (0, styled_1.default)(list_1.default) `
  li {
    padding-left: ${(0, space_1.default)(3)};
    word-break: break-all;
    :before {
      border-color: ${p => p.theme.white};
      top: 6px;
    }
  }
`;
const TooltipTitle = (0, styled_1.default)('div') `
  text-align: left;
`;
const StyledIconWarning = (0, styled_1.default)(icons_1.IconWarning) `
  vertical-align: middle;
`;
//# sourceMappingURL=index.jsx.map