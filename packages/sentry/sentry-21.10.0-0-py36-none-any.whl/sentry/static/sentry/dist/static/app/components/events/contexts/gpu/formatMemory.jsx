Object.defineProperty(exports, "__esModule", { value: true });
const utils_1 = require("app/utils");
const MEGABYTE_IN_BYTES = 1048576;
function formatMemory(memory_size) {
    if (!Number.isInteger(memory_size) || memory_size <= 0) {
        return null;
    }
    // 'usable_memory' is in defined in MB
    return (0, utils_1.formatBytesBase2)(memory_size * MEGABYTE_IN_BYTES);
}
exports.default = formatMemory;
//# sourceMappingURL=formatMemory.jsx.map