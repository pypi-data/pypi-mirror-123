Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const exceptionMechanism_1 = (0, tslib_1.__importDefault)(require("app/components/events/interfaces/exceptionMechanism"));
const annotated_1 = (0, tslib_1.__importDefault)(require("app/components/events/meta/annotated"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const stacktrace_1 = require("app/types/stacktrace");
const exceptionStacktraceContent_1 = (0, tslib_1.__importDefault)(require("./exceptionStacktraceContent"));
const exceptionTitle_1 = (0, tslib_1.__importDefault)(require("./exceptionTitle"));
const ExceptionContent = ({ newestFirst, event, stackView, groupingCurrentLevel, hasHierarchicalGrouping, platform, values, type, }) => {
    if (!values) {
        return null;
    }
    const children = values.map((exc, excIdx) => (<div key={excIdx} className="exception">
      <exceptionTitle_1.default type={exc.type} exceptionModule={exc === null || exc === void 0 ? void 0 : exc.module}/>
      <annotated_1.default object={exc} objectKey="value" required>
        {value => <StyledPre className="exc-message">{value}</StyledPre>}
      </annotated_1.default>
      {exc.mechanism && <exceptionMechanism_1.default data={exc.mechanism}/>}
      <exceptionStacktraceContent_1.default data={type === stacktrace_1.STACK_TYPE.ORIGINAL
            ? exc.stacktrace
            : exc.rawStacktrace || exc.stacktrace} stackView={stackView} stacktrace={exc.stacktrace} expandFirstFrame={excIdx === values.length - 1} platform={platform} newestFirst={newestFirst} event={event} chainedException={values.length > 1} hasHierarchicalGrouping={hasHierarchicalGrouping} groupingCurrentLevel={groupingCurrentLevel}/>
    </div>));
    if (newestFirst) {
        children.reverse();
    }
    return <div>{children}</div>;
};
exports.default = ExceptionContent;
const StyledPre = (0, styled_1.default)('pre') `
  margin-bottom: ${(0, space_1.default)(1)};
  margin-top: 0;
`;
//# sourceMappingURL=exceptionContent.jsx.map