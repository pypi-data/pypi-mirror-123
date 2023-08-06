Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const errorLevel_1 = (0, tslib_1.__importDefault)(require("app/components/events/errorLevel"));
const overflowEllipsis_1 = (0, tslib_1.__importDefault)(require("app/styles/overflowEllipsis"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const BaseEventMessage = ({ className, level, levelIndicatorSize, message, annotations, }) => (<div className={className}>
    {level && (<StyledErrorLevel size={levelIndicatorSize} level={level}>
        {level}
      </StyledErrorLevel>)}

    {message && <Message>{message}</Message>}

    {annotations}
  </div>);
const EventMessage = (0, styled_1.default)(BaseEventMessage) `
  display: flex;
  align-items: center;
  position: relative;
  line-height: 1.2;
  overflow: hidden;
`;
const StyledErrorLevel = (0, styled_1.default)(errorLevel_1.default) `
  margin-right: ${(0, space_1.default)(1)};
`;
const Message = (0, styled_1.default)('span') `
  ${overflowEllipsis_1.default}
  width: auto;
  max-height: 38px;
`;
exports.default = EventMessage;
//# sourceMappingURL=eventMessage.jsx.map