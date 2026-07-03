import { check, group, sleep } from "k6";
import http from "k6/http";
import { Rate, Trend, Counter } from "k6/metrics";

const BASE_URL = __ENV.BASE_URL || "http://localhost:8069";

const loginFailRate = new Rate("login_failures");
const orderFailRate = new Rate("order_failures");
const responseTime = new Trend("response_time_ms");
const orderTime = new Trend("order_time_ms");
const totalOrders = new Counter("total_orders");

export const options = {
  stages: [
    { duration: "30s", target: 5 },
    { duration: "1m", target: 20 },
    { duration: "30s", target: 50 },
    { duration: "1m", target: 50 },
    { duration: "30s", target: 0 },
  ],
  thresholds: {
    http_req_duration: ["p(95)<3000"],
    login_failures: ["rate<0.1"],
    order_failures: ["rate<0.05"],
  },
  noConnectionReuse: true,
};

export default function () {
  group("POS User Session", () => {
    const session = startSession();
    if (!session) {
      loginFailRate.add(1);
      return;
    }

    group("Browse Products", () => {
      browseProducts(session);
    });

    group("Create Order", () => {
      createOrder(session);
    });

    group("View Orders", () => {
      viewOrders(session);
    });

    logout(session);
  });

  sleep(Math.random() * 3 + 1);
}

function startSession() {
  const start = Date.now();

  const loginRes = http.post(`${BASE_URL}/web/session/authenticate`, {
    jsonrpc: "2.0",
    method: "call",
    params: {
      db: "pos_test",
      login: "admin",
      password: "admin",
    },
  });

  responseTime.add(Date.now() - start);

  const success = check(loginRes, {
    "login successful": (r) => r.status === 200,
  });

  if (!success) return null;

  const cookies = loginRes.headers["Set-Cookie"] || "";
  return { cookies };
}

function browseProducts(session) {
  const start = Date.now();

  const res = http.get(`${BASE_URL}/web/dataset/search_read`, {
    headers: {
      Cookie: session.cookies,
      "Content-Type": "application/json",
    },
  });

  responseTime.add(Date.now() - start);

  check(res, {
    "products fetched": (r) => r.status === 200,
  });
}

function createOrder(session) {
  const start = Date.now();

  const orderPayload = {
    jsonrpc: "2.0",
    method: "call",
    params: {
      pos_order: {
        lines: [
          [0, 0, {
            product_id: 1,
            qty: 1,
            price_unit: 100.0,
          }],
        ],
        payment_ids: [
          [0, 0, {
            payment_method_id: 1,
            amount: 100.0,
          }],
        ],
      },
    },
  };

  const res = http.post(`${BASE_URL}/pos/order/create`, JSON.stringify(orderPayload), {
    headers: {
      Cookie: session.cookies,
      "Content-Type": "application/json",
    },
  });

  const elapsed = Date.now() - start;
  orderTime.add(elapsed);
  totalOrders.add(1);

  const success = check(res, {
    "order created": (r) => r.status === 200,
  });

  if (!success) orderFailRate.add(1);
}

function viewOrders(session) {
  const res = http.get(`${BASE_URL}/web/dataset/search_read?model=pos.order`, {
    headers: {
      Cookie: session.cookies,
    },
  });

  check(res, {
    "orders retrieved": (r) => r.status === 200,
  });
}

function logout(session) {
  http.post(`${BASE_URL}/web/session/destroy`, {}, {
    headers: {
      Cookie: session.cookies,
    },
  });
}
