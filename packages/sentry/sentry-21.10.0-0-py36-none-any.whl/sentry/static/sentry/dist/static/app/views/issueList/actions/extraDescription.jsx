Object.defineProperty(exports, "__esModule", { value: true });
const locale_1 = require("app/locale");
const utils_1 = require("./utils");
function ExtraDescription({ all, query, queryCount }) {
    if (!all) {
        return null;
    }
    if (query) {
        return (<div>
        <p>{(0, locale_1.t)('This will apply to the current search query') + ':'}</p>
        <pre>{query}</pre>
      </div>);
    }
    return (<p className="error">
      <strong>
        {queryCount > utils_1.BULK_LIMIT
            ? (0, locale_1.tct)('This will apply to the first [bulkNumber] issues matched in this project!', {
                bulkNumber: utils_1.BULK_LIMIT_STR,
            })
            : (0, locale_1.tct)('This will apply to all [bulkNumber] issues matched in this project!', {
                bulkNumber: queryCount,
            })}
      </strong>
    </p>);
}
exports.default = ExtraDescription;
//# sourceMappingURL=extraDescription.jsx.map