

class CTest {
    // Cyclomatic ： 9
    void test1() {
        int a = 20;

        if (a>10) {
            a = 5;
        }

        while (a>30) {
            a = 20;
        }

        for (a=20; a>30; a++) {
            a = 20;
        }

        do {
            a = 20;
        } while (a>30);

        a = a>30?20:40;

        switch(a) {
            case 2:
                break;
            case 3:
                break;
            case 4: 
                break;
            default:
                break;
        }
    }

    // Cyclomatic: 3
    void test2() {
        int a = 20;

        if (a>10) {
            a = 5;
        }

        while (a>30) {
            a = 20;
        }

        try {
            a = 20;
        } catch(Exception e) {
            a = 30;
        }

    }
}
