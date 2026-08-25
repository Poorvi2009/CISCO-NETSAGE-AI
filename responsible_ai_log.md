# Responsible AI & Human Review Log
**System:** NetSage AI Troubleshooting Assistant
**Requirement:** Minimum 5 cases where AI initial diagnosis was corrected/edited by Human Reviewer.

| Case ID | Symptom | AI Initial Diagnosis | Human Review Decision | Human Corrective Action & Reason |
| :--- | :--- | :--- | :--- | :--- |
| **NET-003** | PC1 can ping 8.8.8.8 but cannot open google.com | Recommended changing local DNS IP on client PC to 8.8.8.8. | **Edited** | **Correction:** AI missed router configuration. Re-enabled `ip domain-lookup` on gateway router and verified active internal DNS server `192.168.1.5` per network policy. |
| **NET-008** | OSPF neighbor stuck in INIT state | AI diagnosed Layer 1 cable issue and suggested re-seating physical connection. | **Rejected** | **Correction:** Layer 1 was UP/UP. Show output showed mismatched OSPF MTU sizes (1500 vs 1400). Solution was adding `ip ospf mtu-ignore` or updating MTU. |
| **NET-014** | Switch port constantly flapping between Forwarding/Blocking | AI reported bad physical port or faulty SFP module. | **Edited** | **Correction:** Show output contained `PortFast` enabled on switch-to-switch trunk port causing temporary Spanning Tree Loops. Removed PortFast from trunk interface. |
| **NET-022** | Wireless client fails 802.1X authentication | AI recommended rebooting the Wireless LAN Controller (WLC). | **Rejected** | **Correction:** RADIUS shared key mismatch was shown in RADIUS log output. Re-entered matching pre-shared key on RADIUS server and WLC. |
| **NET-029** | Dynamic NAT working for HTTP but failing for SSH | AI suggested global NAT pool exhaustion. | **Edited** | **Correction:** NAT pool had available addresses; extended ACL backing NAT statement omitted TCP port 22 (`permit ip` vs explicit match). Modified ACL to permit all IP traffic for translation. |

---

### Key Takeaways for Governance & Safety
1. **Hallucination Safeguards:** AI models tend to recommend physical replacement or reboots when complex protocol mismatches occur.
2. **Context Limits:** Human validation ensures fixes adhere to local enterprise security policies rather than generic workarounds.