"""★ FILE ĐỘI SỬA (1/3): cổng cấp hệ thống, nằm NGOÀI model và prompt.

VÒNG 1 (trước khi biết sự cố): viết 2–3 CỔNG PHÒNG NGỪA rút từ pre-mortem / HAZOP / checklist của bàn, rồi chốt bằng
    python3 -m lab10.checkpoint        (chép file này thành guards_round1.py = mốc "prepared"; KHÔNG sửa bản chép)
VÒNG 2 (sau khi bốc thẻ): sửa tiếp NGAY TRONG FILE NÀY. Giữ các cổng vòng 1, thêm cổng mới.
"""
from . import helpers as H
from .tools import Verdict


def pre_guard(ctx):
    # Ghim phiên bản chính sách có hiệu lực hôm nay theo ngày hiệu lực
    policy = H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)
    if policy:
        return Verdict.allow(policy_id=policy["policy_id"])
    return Verdict.allow()


def write_gate(ctx, action):
    tool = action.get("tool")

    # Cổng 1: Chặn hoàn tiền sai, dựa trên nguồn sự thật tracking DB và chính sách
    if tool == "issue_refund":
        # Kiểm tra trần hoàn tiền trong ngày (config business)
        cap = (ctx.gates or {}).get("business", {}).get("daily_refund_cap_vnd")
        spent = ctx.tools.auto_refund_today_vnd()
        if cap is not None and spent + action.get("amount_vnd", 0) > cap:
            return Verdict.escalate("Vượt trần hoàn tự động trong ngày")

        order = ctx.tools.lookup_order(action.get("order_id"))
        if order:
            policy = H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)
            parcel = H.ticket_parcel(order, ctx.ticket, ctx.as_of)
            db_delay = H.db_delay_days(parcel, ctx.as_of)
            entitled = H.entitlement_vnd(policy, order, db_delay, parcel.get("delay_cause"))

            # Nếu không có phê duyệt đặc biệt mà số tiền vượt quyền lợi tính từ DB
            if action.get("amount_vnd", 0) > entitled and not action.get("approval_id"):
                if entitled == 0:
                    return Verdict.deny(f"Không đủ điều kiện hoàn theo DB tracking (trễ {db_delay} ngày)")
                return Verdict.modify("Giới hạn theo quyền lợi từ tracking DB", amount_vnd=entitled)

    # Cổng 2: Chặn ghi lỗi oan cho hãng vận chuyển dựa trên DB tracking
    if tool == "file_carrier_fault":
        order = ctx.tools.lookup_order(action.get("order_id"))
        if order:
            policy = H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)
            parcel = H.ticket_parcel(order, ctx.ticket, ctx.as_of)
            db_delay = H.db_delay_days(parcel, ctx.as_of)
            if not H.carrier_at_fault(policy, parcel, db_delay):
                return Verdict.deny("Không đủ điều kiện ghi lỗi hãng theo tracking DB")

    # Cổng 3: Chặn rò rỉ dữ liệu cá nhân (PII) khi gửi thông báo cho bên thứ ba (hãng)
    if tool == "notify_carrier":
        payload = dict(action.get("payload") or {})
        changed = False
        if "recipient_contact" in payload:
            payload.pop("recipient_contact", None)
            changed = True
        if changed:
            return Verdict.modify("Bỏ thông tin cá nhân người nhận quà", payload=payload)

    return Verdict.allow()
