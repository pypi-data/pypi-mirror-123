Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const model_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/model"));
class MonitorModel extends model_1.default {
    getTransformedData() {
        return this.fields.toJSON().reduce((data, [k, v]) => {
            if (k.indexOf('config.') !== 0) {
                data[k] = v;
                return data;
            }
            if (!data.config) {
                data.config = {};
            }
            if (k === 'config.schedule.frequency' || k === 'config.schedule.interval') {
                if (!Array.isArray(data.config.schedule)) {
                    data.config.schedule = [null, null];
                }
            }
            if (k === 'config.schedule.frequency') {
                data.config.schedule[0] = parseInt(v, 10);
            }
            else if (k === 'config.schedule.interval') {
                data.config.schedule[1] = v;
            }
            else {
                data.config[k.substr(7)] = v;
            }
            return data;
        }, {});
    }
    getTransformedValue(id) {
        return id.indexOf('config') === 0 ? this.getValue(id) : super.getTransformedValue(id);
    }
}
exports.default = MonitorModel;
//# sourceMappingURL=monitorModel.jsx.map