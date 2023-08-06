Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const redaction_1 = (0, tslib_1.__importDefault)(require("./redaction"));
const utils_1 = require("./utils");
const Chunk = ({ chunk }) => {
    if (chunk.type === 'redaction') {
        const title = (0, utils_1.getTooltipText)({ rule_id: chunk.rule_id, remark: chunk.remark });
        return (<tooltip_1.default title={title}>
        <redaction_1.default>{chunk.text}</redaction_1.default>
      </tooltip_1.default>);
    }
    return <span>{chunk.text}</span>;
};
exports.default = Chunk;
//# sourceMappingURL=chunk.jsx.map