Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const marked_1 = (0, tslib_1.__importDefault)(require("app/utils/marked"));
const NoteBody = ({ className, text }) => (<div className={className} data-test-id="activity-note-body" dangerouslySetInnerHTML={{ __html: (0, marked_1.default)(text) }}/>);
exports.default = NoteBody;
//# sourceMappingURL=body.jsx.map