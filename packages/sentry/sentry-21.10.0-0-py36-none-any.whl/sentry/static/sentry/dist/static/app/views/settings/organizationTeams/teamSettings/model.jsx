Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const teams_1 = require("app/actionCreators/teams");
const model_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/model"));
class TeamFormModel extends model_1.default {
    constructor(orgId, teamId) {
        super();
        this.orgId = orgId;
        this.teamId = teamId;
    }
    doApiRequest({ data }) {
        return new Promise((resolve, reject) => (0, teams_1.updateTeam)(this.api, {
            orgId: this.orgId,
            teamId: this.teamId,
            data,
        }, {
            success: resolve,
            error: reject,
        }));
    }
}
exports.default = TeamFormModel;
//# sourceMappingURL=model.jsx.map